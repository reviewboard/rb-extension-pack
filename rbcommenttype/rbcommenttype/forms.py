from __future__ import unicode_literals

import json

from django.forms import BooleanField, Field, Widget
from django.forms.utils import flatatt
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from djblets.extensions.forms import SettingsForm


class CommentTypesWidget(Widget):
    """A form widget for configuring comment types."""

    def render(self, name, value, attrs=None):
        """Render the widget."""
        attrs = self.build_attrs(attrs, {
            'type': 'hidden',
            'name': name,
        })

        if value:
            attrs['value'] = json.dumps(value)

        return format_html('<input{0} />', flatatt(attrs))


class CommentTypesField(Field):
    """A form field for configuring comment types."""

    widget = CommentTypesWidget

    def __init__(self, *args, **kwargs):
        """Initialize the field."""
        super(CommentTypesField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        """Return a python dictionary mapping ID to comment type."""
        return json.loads(value)


class CommentTypeSettingsForm(SettingsForm):
    """Settings form for comment type categorization."""

    require_type = BooleanField(
        initial=False,
        required=False,
        label=_('Require comment type'),
        help_text=_('Require users to select a comment type for every '
                    'new comment.'))
    types = CommentTypesField(required=True)
