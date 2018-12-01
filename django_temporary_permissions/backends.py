from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Permission
from django.utils import timezone
from django_temporary_permissions.models import TemporaryGroupPermissions


class TempPermissionsBackend(ModelBackend):

    def get_group_permissions(self, user_obj, obj=None):
        """
        Returns a set of permission strings active that this user has through his/her
        groups plus the permissions active in this moment.
        """
        if user_obj.is_anonymous or obj is not None:
            if settings.MANAGE_ANONYMOUS_USER:
                user_obj = get_user_model().objects.get(pk=settings.ANONYMOUS_USERID)
            else:
                return set()
        if user_obj.is_superuser:
            perms = Permission.objects.all()
        else:
            today = timezone.now()
            active_groups = TemporaryGroupPermissions.objects.filter(user=user_obj,
                                                                     from_date__lte=today,
                                                                     to_date__gte=today).select_related()
            perms = Permission.objects.filter(group__in=[tgp.group for tgp in active_groups])

        perms = perms.values_list('content_type__app_label', 'codename').order_by()
        user_obj._group_perm_cache = set(["%s.%s" % (ct, name) for ct, name in perms])
        return user_obj._group_perm_cache

    def get_all_permissions(self, user_obj, obj=None):
        if user_obj.is_anonymous or obj is not None:
            if settings.MANAGE_ANONYMOUS_USER:
                user_obj = get_user_model().objects.get(pk=settings.ANONYMOUS_USERID)
            else:
                return set()
        if not hasattr(user_obj, '_perm_cache'):
            user_obj._perm_cache = set([u"%s.%s" % (p.content_type.app_label, p.codename)
                                        for p in user_obj.user_permissions.select_related()])
        user_obj._perm_cache.update(self.get_group_permissions(user_obj))
        return user_obj._perm_cache

    def has_perm(self, user_obj, perm, obj=None):
        if not user_obj.is_active:
            return False
        return perm in self.get_all_permissions(user_obj, obj)
