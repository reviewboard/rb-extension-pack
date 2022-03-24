"""Comment severity extension for Review Board."""

from reviewboard.extensions.base import Extension, JSExtension
from reviewboard.extensions.hooks import CommentDetailDisplayHook
from reviewboard.urls import reviewable_url_names, review_request_url_names


apply_to_url_names = set(reviewable_url_names + review_request_url_names)


class SeverityCommentDetailDisplay(CommentDetailDisplayHook):
    """Adds the severity information to displayed comments.

    This extends the comments in the review dialog and in the e-mails
    to show the selected severity.
    """

    SEVERITY_LABELS = {
        'major': 'Major',
        'minor': 'Minor',
        'info': 'Info',
    }

    HTML_EMAIL_COMMON_SEVERITY_CSS = (
        'font-weight: bold;'
        'font-size: 9pt;'
    )

    HTML_EMAIL_SPECIFIC_SEVERITY_CSS = {
        'major': 'color: #AA0000;',
        'minor': 'color: #CC5500;',
        'info': 'color: #006600;',
    }

    def render_review_comment_detail(self, comment):
        """Render the severity of a comment on a review.

        Args:
            comment (reviewboard.reviews.models.BaseComment):
                The comment to render for.

        Returns:
            str:
            The rendered HTML.
        """
        severity = comment.extra_data.get('severity')

        if not severity:
            return ''

        return ('<p class="comment-severity comment-severity-%s">'
                'Severity: %s'
                '</p>'
                % (severity, self._get_severity_label(severity)))

    def render_email_comment_detail(self, comment, is_html):
        """Render the severity of a comment on an e-mail.

        Args:
            comment (reviewboard.reviews.models.BaseComment):
                The comment to render for.

            is_html (boolean):
                Whether to render HTML or plain text.

        Returns:
            str:
            The rendered comment severity.
        """
        severity = comment.extra_data.get('severity')

        if not severity:
            return ''

        if is_html:
            specific_css = self.HTML_EMAIL_SPECIFIC_SEVERITY_CSS.get(
                severity, '')

            return ('<p style="%s%s">Severity: %s</p>'
                    % (self.HTML_EMAIL_COMMON_SEVERITY_CSS,
                       specific_css,
                       self._get_severity_label(severity)))
        else:
            return '[Severity: %s]\n' % self._get_severity_label(severity)

    def _get_severity_label(self, severity):
        return self.SEVERITY_LABELS.get(severity, 'Unknown')


class SeverityJSExtension(JSExtension):
    """Javascript extension for the severity extension."""

    model_class = 'RBSeverity.Extension'
    apply_to = apply_to_url_names


class SeverityExtension(Extension):
    """Extends Review Board with comment severity support.

    When creating or updating comments, users will be required to set a
    severity level. This level will appear in the reviews, in e-mails, and
    in the API (through the comment's extra_data).
    """

    metadata = {
        'Name': 'Comment Severity',
    }

    js_extensions = [SeverityJSExtension]

    css_bundles = {
        'default': {
            'source_filenames': ['css/severity.less'],
            'apply_to': apply_to_url_names,
        }
    }

    js_bundles = {
        'severity-review': {
            'source_filenames': ['js/severity.es6.js'],
            'apply_to': apply_to_url_names,
        }
    }

    def initialize(self):
        """Initialize the extension."""
        SeverityCommentDetailDisplay(self)
