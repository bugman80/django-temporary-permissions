
from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import ugettext_lazy as _


class TemporaryGroupPermissionsManager(models.Manager):
    def get_by_natural_key(self, user, group, from_date, to_date):
        return self.get(user=user, group=group, from_date=from_date, to_date=to_date)


class TemporaryGroupPermissions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    from_date = models.DateTimeField(help_text='Use UTC timezone')
    to_date = models.DateTimeField(help_text='Use UTC timezone')

    objects = TemporaryGroupPermissionsManager()

    class Meta:
        verbose_name_plural = _('Temporary Group Permissions')

    def natural_key(self):
        return self.user, self.group, self.from_date, self.to_date

    def __unicode__(self):
        return u'%s - %s' % (self.user, self.group)
