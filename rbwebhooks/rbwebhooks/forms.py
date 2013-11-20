from django import forms
from django.utils.translation import ugettext as _

from djblets.extensions.forms import SettingsForm


class WebHooksSettingsForm(SettingsForm):
    username = forms.CharField(max_length=64,
        help_text=_("Basic auth username to use for POST requests"))
    password = forms.CharField(max_length=64, widget=forms.PasswordInput(),
        help_text=_("Basic auth password to use for POST requests"))
    attempts = forms.IntegerField(min_value=0, initial=1,
        help_text=_("The number of times to attempt each request."))
