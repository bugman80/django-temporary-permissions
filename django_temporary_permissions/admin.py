from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django_temporary_permissions.forms import TemporaryGroupPermissionsForm
from django_temporary_permissions.models import TemporaryGroupPermissions


class TemporaryGroupPermissionsAdmin(ModelAdmin):
    list_filter = ('user', 'group', 'from_date', 'to_date')
    search_fields = ['user__username', 'group__name']
    actions = ['delete_expired_permissions']
    form = TemporaryGroupPermissionsForm

    def delete_expired_permissions(self, request, qs):
        today = timezone.now()
        for temp_perm in qs:
            if temp_perm.to_date < today:
                temp_perm.delete()
        self.message_user(request, _('Expired Temporary Permissions successfully deleted.'))

admin.site.register(TemporaryGroupPermissions, TemporaryGroupPermissionsAdmin)
