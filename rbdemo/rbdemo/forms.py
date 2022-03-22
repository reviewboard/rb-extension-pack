"""Forms for the demo server extension."""

import re

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from djblets.extensions.forms import SettingsForm
from reviewboard.reviews.models import Group


class DemoAuthSettingsForm(SettingsForm):
    """Configuration form for the demo authentication settings."""

    auth_user_prefix = forms.CharField(
        label=_('Username prefix'),
        help_text=_('The prefix that generated usernames will start with.'))

    auth_user_max_id = forms.IntegerField(
        label=_('Max numeric suffix on username'),
        help_text=_('The maximum number used for generating the numeric '
                    'suffix for the username.'))

    auth_password = forms.CharField(
        label=_('Demo password'),
        help_text=_('The password used for authenticating to any demo user.'))

    auth_default_groups = forms.CharField(
        label=_('Default groups'),
        help_text=_('Comma-separated list of default group names.'),
        widget=forms.TextInput(attrs={'size': 40}),
        required=False)

    def __init__(self, siteconfig, *args, **kwargs):
        """Initialize the form.

        Args:
            siteconfig (djblets.siteconfig.models.SiteConfiguration):
                The siteconfig object.

            *args (tuple):
                Positional arguments to pass to the base class.

            **kwargs (dict):
                Keyword arguments to pass to the base class.
        """
        from rbdemo.extension import DemoExtension

        super(DemoAuthSettingsForm, self).__init__(
            DemoExtension.instance, *args, **kwargs)

    def clean_auth_default_groups(self):
        """Validate and serialize a list of groups.

        Returns:
            list of reviewboard.reviews.models.Group:
            The list of groups to add new users to.
        """
        group_list = re.split(r',\s*',
                              self.cleaned_data['auth_default_groups'])

        for group_name in group_list:
            try:
                Group.objects.get(name=group_name)
            except Group.DoesNotExist:
                raise ValidationError(
                    _('%(group_name)s is not a valid group'),
                    params={
                        'group_name': group_name,
                    },
                    code='invalid-group')

        return group_list

    def load(self):
        """Load the initial form data."""
        super(DemoAuthSettingsForm, self).load()

        self.fields['auth_default_groups'].initial = \
            ', '.join(self.settings['auth_default_groups'])

    class Meta:
        """Metadata for the config form."""

        title = _('Demo Authentication Settings')
