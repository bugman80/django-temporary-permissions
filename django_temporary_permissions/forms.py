from django.core.exceptions import ValidationError
from django.forms import ModelForm

from django_temporary_permissions.models import TemporaryGroupPermissions


class TemporaryGroupPermissionsForm(ModelForm):
    class Meta:
        model = TemporaryGroupPermissions
        # fields = '__all__'  #  to replace the next line once support for 1.5 will be dropped
        fields = (
            'user',
            'group',
            'from_date',
            'to_date',
        )

    def clean(self):
        # verify mandatory field
        conditions = [
            not self.cleaned_data.get('user', None),
            not self.cleaned_data.get('group', None),
            not self.cleaned_data.get('from_date', None),
            not self.cleaned_data.get('to_date', None),
        ]

        if any(conditions):
            raise ValidationError('Please fill the fields below:')

        # Don't allow entries with a from_date <= to_date
        if not self.cleaned_data['from_date'] < self.cleaned_data['to_date']:
            raise ValidationError('Invalid date, please enter a valid period')

        qs = self.cleaned_data.get('user').temporarygrouppermissions_set

        qs = qs.filter(group=self.cleaned_data.get('group'),
                       from_date__lt=self.cleaned_data.get('to_date'),
                       to_date__gt=self.cleaned_data.get('from_date'))

        if self.cleaned_data.get('id', None):
            qs = qs.exclude(pk=self.cleaned_data.get('id').pk)

        overlap = qs.exists()

        if overlap:
            raise ValidationError('Period overlapping a previously entered one for the same user and group')

        return self.cleaned_data
