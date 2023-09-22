import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        # Here we're getting the data from the default data cleaning method, which sanitizes
        # the data and removes unsafe data, as well as converts it to the correct Python type
        data = self.cleaned_data['renewal_date']

        # Another note, we use gettext_lazy as _ to wrap our text so that we can translate
        # the website at a later time easily

        # Check to ensure date isn't in the past
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal is in past'))

        # Check to ensure date is in allowed time frame (4 weeks from today)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # return cleaned data
        return data
