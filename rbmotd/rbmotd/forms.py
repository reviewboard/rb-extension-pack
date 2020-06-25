"""Forms for the rbmotd extension."""

from __future__ import unicode_literals

import hashlib

from django import forms
from django.utils.translation import ugettext as _
from djblets.extensions.forms import SettingsForm


class MotdSettingsForm(SettingsForm):
    """The settings form for the motd extension."""

    enabled = forms.BooleanField(initial=False, required=False)
    message = forms.CharField(
        max_length=512,
        required=False,
        help_text=_('This field expects valid HTML. Entities must be '
                    'properly escaped.'),
        widget=forms.TextInput(attrs={
            'size': 100,
        }))

    def set_key_value(self, key, value):
        """Set the given value in the extension settings.

        This overrides the base settings form method so that when the
        ``message`` key is set, it will additionally compute and store a
        ``message_id`` key.

        Args:
            key (unicode):
                The key to set.

            value (object):
                The value to set.
        """
        if key == 'message':
            message_id = hashlib.sha256(value).hexdigest()
            self.set_key_value('message_id', message_id)

        super(MotdSettingsForm, self).set_key_value(key, value)
