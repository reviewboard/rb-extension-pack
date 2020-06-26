"""Forms for the rbwebhooks extension."""

from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext as _
from djblets.extensions.forms import SettingsForm


class WebHooksSettingsForm(SettingsForm):
    """Settings form for the rbwebhooks extension."""

    attempts = forms.IntegerField(
        min_value=0,
        initial=1,
        help_text=_('The number of times to attempt each request.'))
