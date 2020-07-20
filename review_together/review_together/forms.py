"""Forms for the Review Together extension."""

from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _
from djblets.extensions.forms import SettingsForm


class ReviewTogetherSettingsForm(SettingsForm):
    """Settings form for the Review Together extension."""

    hub_url = forms.CharField(label=_('TogetherJS Hub URL'), required=False)
