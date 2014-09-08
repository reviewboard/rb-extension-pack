from django import forms
from django.utils.translation import ugettext_lazy as _
from djblets.extensions.forms import SettingsForm


class ReviewTogetherSettingsForm(SettingsForm):
    hub_url = forms.CharField(label=_("TogetherJS Hub URL"), required=False)
