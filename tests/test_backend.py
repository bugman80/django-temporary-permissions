from django_dynamic_fixture import G

from django.conf import settings
from django.contrib.auth.hashers import MD5PasswordHasher
from django.contrib.auth.models import AnonymousUser, Group, Permission, User
from django.test import TestCase
from django.utils import timezone
from django_temporary_permissions.forms import TemporaryGroupPermissionsForm
from django_temporary_permissions.models import TemporaryGroupPermissions


class TestBackendPermKnownUser(TestCase):
    def setUp(self):
        self.user = G(User, password=MD5PasswordHasher().encode('fakePassword', 'salt'))
        self.perm1 = G(Permission)
        self.perm2 = G(Permission)
        self.perm3 = G(Permission)
        self.perm4 = G(Permission)
        self.group1 = G(Group, permissions=(self.perm1, self.perm2))
        self.group2 = G(Group, permissions=(self.perm3, self.perm4))
        today = timezone.now()
        self.inactive_from = today + timezone.timedelta(days=-2)
        self.inactive_to = today + timezone.timedelta(days=-1)
        self.active_from = today + timezone.timedelta(days=-2)
        self.active_to = today + timezone.timedelta(days=2)

    def test_group_permissions(self):
        G(TemporaryGroupPermissions,
          user=self.user,
          group=self.group1,
          from_date=self.inactive_from,
          to_date=self.inactive_to)

        G(TemporaryGroupPermissions,
          user=self.user,
          group=self.group2,
          from_date=self.active_from,
          to_date=self.active_to)

        self.assertTrue(self.user.has_perm(self.perm3.content_type.app_label + '.' + self.perm3.codename))
        self.assertTrue(self.user.has_perm(self.perm4.content_type.app_label + '.' + self.perm4.codename))
        self.assertFalse(self.user.has_perm(self.perm1.content_type.app_label + '.' + self.perm1.codename))
        self.assertFalse(self.user.has_perm(self.perm2.content_type.app_label + '.' + self.perm2.codename))


class TestBackendPermAnonymousUser(TestCase):
    def setUp(self):
        self.perm1 = G(Permission)
        self.perm2 = G(Permission)
        self.perm3 = G(Permission)
        self.perm4 = G(Permission)
        self.group1 = G(Group, permissions=(self.perm1, self.perm2))
        self.group2 = G(Group, permissions=(self.perm3, self.perm4))
        today = timezone.now()
        self.inactive_from = today + timezone.timedelta(days=-2)
        self.inactive_to = today + timezone.timedelta(days=-1)
        self.active_from = today + timezone.timedelta(days=-2)
        self.active_to = today + timezone.timedelta(days=2)

    def test_anonymous_permissions(self):
        anonymous_user = AnonymousUser()
        anonymous_user.is_active = True

        with self.settings(TEMP_PERMISSIONS_MANAGE_ANONYMOUS_USER=True, TEMP_PERMISSIONS_ANONYMOUS_USERID=999):
            user = G(User, id=settings.ANONYMOUS_USERID, password=MD5PasswordHasher().encode('fakePassword', 'salt'))

            G(TemporaryGroupPermissions,
              user=user,
              group=self.group1,
              from_date=self.inactive_from,
              to_date=self.inactive_to)

            G(TemporaryGroupPermissions,
              user=user,
              group=self.group2,
              from_date=self.active_from,
              to_date=self.active_to)

            self.assertTrue(anonymous_user.has_perm(self.perm3.content_type.app_label + '.' + self.perm3.codename))
            self.assertTrue(anonymous_user.has_perm(self.perm4.content_type.app_label + '.' + self.perm4.codename))
            self.assertFalse(anonymous_user.has_perm(self.perm1.content_type.app_label + '.' + self.perm1.codename))
            self.assertFalse(anonymous_user.has_perm(self.perm2.content_type.app_label + '.' + self.perm2.codename))


class TestManager(TestCase):

    def test_group_natural_key(self):
        group = G(Group)
        today = timezone.now()
        date_from = today
        date_to = today + timezone.timedelta(days=+1)
        target = G(TemporaryGroupPermissions, group=group, from_date=date_from, to_date=date_to)
        self.assertTrue(TemporaryGroupPermissions.objects.get_by_natural_key(*target.natural_key()))


class TestModel(TestCase):

    def test_invalid_date(self):
        perm1 = G(Permission)
        group = G(Group, permissions=(perm1, ))
        today = timezone.now()
        date_from = today
        date_to = today
        user = G(User)
        t1 = TemporaryGroupPermissions(user=user, group=group, from_date=date_from, to_date=date_to)
        f1 = TemporaryGroupPermissionsForm(instance=t1)
        self.assertFalse(f1.is_valid())
        date_to = today + timezone.timedelta(days=-1)
        t2 = TemporaryGroupPermissions(user=user, group=group, from_date=date_from, to_date=date_to)
        f2 = TemporaryGroupPermissionsForm(instance=t2)
        self.assertFalse(f2.is_valid())

    def test_overlapping_period(self):
        user = G(User)
        perm1 = G(Permission)
        group = G(Group, permissions=(perm1, ))
        today = timezone.now()
        date_from1 = today
        date_to1 = today + timezone.timedelta(days=30)
        G(TemporaryGroupPermissions, user=user, group=group, from_date=date_from1, to_date=date_to1)
        date_from2 = today + timezone.timedelta(days=10)
        date_to2 = today + timezone.timedelta(days=40)
        t = TemporaryGroupPermissions(user=user, group=group, from_date=date_from2, to_date=date_to2)
        form = TemporaryGroupPermissionsForm(instance=t)
        self.assertFalse(form.is_valid())
