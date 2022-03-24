"""Review Board Extension for adding a "notes" field."""

from django.utils.translation import ugettext_lazy as _
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import ReviewRequestFieldsHook
from reviewboard.reviews.fields import BaseTextAreaField


class NoteField(BaseTextAreaField):
    """The 'Note to Reviewers' field."""

    field_id = 'beanbag_notefield_notes'
    label = _('Note to Reviewers')
    enable_markdown = True

    def render_change_entry_html(self, info):
        """Render the data for the change description.

        Args:
            info (dict):
                The info dict from the ChangeDescription object.

        Returns:
            django.utils.safestring.SafeText:
            The rendered change entry HTML.
        """
        # Work around a bug in Review Board < 2.0.7, where a 'None' value
        # would break change rendering.
        if 'old' in info and info['old'][0] is None:
            info['old'] = ['']

        if 'new' in info and info['new'][0] is None:
            info['new'] = ['']

        return super(NoteField, self).render_change_entry_html(info)


class NoteFieldExtension(Extension):
    """The 'Note to Reviewers' extension."""

    metadata = {
        'Name': _('Note to Reviewers'),
        'Summary': _('Add a "Note to Reviewers" field to review requests, '
                     'for any special instructions not suitable for the '
                     'Description field.'),
    }

    def initialize(self):
        """Initialize the extension."""
        ReviewRequestFieldsHook(self, 'main', [NoteField])
