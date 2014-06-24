from django.utils.translation import ugettext_lazy as _
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import ReviewRequestFieldsHook
from reviewboard.reviews.fields import BaseTextAreaField


class NoteField(BaseTextAreaField):
    field_id = 'beanbag_notefield_notes'
    label = _('Note to Reviewers')
    enable_markdown = True


class NoteFieldExtension(Extension):
    metadata = {
        'Name': _('Note to Reviewers'),
        'Summary': _('Add a "Note to Reviewers" field to review requests, '
                     'for any special instructions not suitable for the '
                     'Description field.'),
    }

    def initialize(self):
        ReviewRequestFieldsHook(self, 'main', [NoteField])
