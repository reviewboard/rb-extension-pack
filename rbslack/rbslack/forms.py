"""Forms definitions for the rbslack extension."""

from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _
from djblets.extensions.forms import SettingsForm


class SlackSettingsForm(SettingsForm):
    """The settings form for the rbslack extension."""

    webhook_url = forms.URLField(
        label=_('Webhook URL'),
        help_text=_('Your unique Slack webhook URL. This can be found in the '
                    '"Setup Instructions" box inside the Incoming WebHooks '
                    'integration.'),
        widget=forms.TextInput(attrs={
            'size': 110,
        }))

    channel = forms.CharField(
        label=_('Send to Channel'),
        required=False,
        help_text=_('The optional name of the channel review request updates '
                    'are sent to. By default, the configured channel on the '
                    'Incoming Webhook will be used.'),
        widget=forms.TextInput(attrs={
            'size': 40,
        }))

    class Meta:
        fieldsets = (
            {
                'description': _(
                    'To start, add a new "Incoming WebHooks" service '
                    'integration on Slack. You can then provide the '
                    '"Unique WebHook URL" below, and optionally choose a '
                    'custom channel to send notifications to.'
                ),
                'fields': ('webhook_url', 'channel'),
                'classes': ('wide',)
            },
        )
