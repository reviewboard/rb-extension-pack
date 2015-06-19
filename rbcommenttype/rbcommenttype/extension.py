from __future__ import unicode_literals

import json

from django.utils.html import format_html
from django.utils.translation import ugettext as _
from reviewboard.extensions.base import Extension, JSExtension
from reviewboard.extensions.hooks import CommentDetailDisplayHook, TemplateHook
from reviewboard.urls import reviewable_url_names, review_request_url_names


apply_to_url_names = set(reviewable_url_names + review_request_url_names)


class CommentTypeCommentDetailDisplay(CommentDetailDisplayHook):
    """Adds detect type information to displayed comments."""

    def render_review_comment_detail(self, comment):
        """Render the comment type to HTML."""
        comment_type = comment.extra_data.get('commentType')

        if not comment_type:
            return ''

        return format_html(
            '<p class="comment-type"><label>{0}</label> {1}</p>',
            _('Type:'), comment_type)


class CommentTypeJSExtension(JSExtension):
    """JavaScript extension for comment types."""

    model_class = 'RBCommentType.Extension'
    apply_to = apply_to_url_names


class CommentTypeExtension(Extension):
    """Extends Review Board with comment comment categorization.

    When creating or updating comments, users will be allowed to choose a
    category for the comment. These categories can be configured in the
    extension settings, and can be fetched from the comment's ``extra_data``
    field.
    """

    metadata = {
        'Name': 'Comment Categorization',
    }

    is_configurable = True

    js_extensions = [CommentTypeJSExtension]

    css_bundles = {
        'comment-type-configure': {
            'source_filenames': ['css/configure.less'],
            'apply_to': 'rbcommenttype-configure',
        }
    }

    js_bundles = {
        'comment-type': {
            'source_filenames': ['js/commentType.js'],
            'apply_to': apply_to_url_names,
        },
        'comment-type-configure': {
            'source_filenames': ['js/configure.js'],
            'apply_to': 'rbcommenttype-configure',
        }
    }

    def initialize(self):
        """Initialize the extension."""
        CommentTypeCommentDetailDisplay(self)

        TemplateHook(self, 'base-scripts-post', 'rbcommenttype-types.html',
                     apply_to=apply_to_url_names)

    @property
    def configured_types(self):
        """Return a list of the configured type names."""
        types = [t['type']
                 for t in self.settings.get('types', [])
                 if t['visible']]

        if not self.settings.get('require_type', False):
            types.insert(0, '')

        return json.dumps(types)
