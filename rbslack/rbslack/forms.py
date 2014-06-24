from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _
from djblets.extensions.forms import SettingsForm


class SlackSettingsForm(SettingsForm):
    webhook_url = forms.URLField(
        help_text=_('Your unique Slack webhook URL. This can be found in the '
                    '"Setup Instructions" box inside the Incoming Webhooks '
                    'integration.'))
    channel = forms.CharField(
        help_text=_('The name of the channel review request updates are sent '
                    'to.'))
