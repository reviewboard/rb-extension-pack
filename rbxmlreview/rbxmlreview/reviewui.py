"""Review UI for XML files."""

from __future__ import unicode_literals

import logging

import pygments
from django.utils.encoding import force_unicode
from django.utils.functional import cached_property
from reviewboard.reviews.ui.base import FileAttachmentReviewUI


class XMLReviewUI(FileAttachmentReviewUI):
    """Review UI for XML files."""

    name = 'XML'
    supported_mimetypes = ['application/xml', 'text/xml']

    js_model_class = 'RB.XMLReviewable'
    js_view_class = 'RB.XMLReviewableView'

    def __init__(self, review_request, obj):
        """Initialize the review UI.

        Args:
            review_request (reviewboard.reviews.models.ReviewRequest):
                The review request.

            obj (reviewboard.attachments.models.FileAttachment):
                The file being reviewed.
        """
        super(XMLReviewUI, self).__init__(review_request, obj)

        from rbxmlreview.extension import XMLReviewUIExtension
        self.extension = XMLReviewUIExtension.instance

    @cached_property
    def js_bundle_names(self):
        """The list of JavaScript bundles for the review UI."""
        return [
            self.extension.get_bundle_id('xmlreviewable'),
        ]

    def get_js_model_data(self):
        """Return the data for the JavaScript model.

        Returns:
            dict:
            Data to pass through to RB.XMLReviewable.
        """
        data = super(XMLReviewUI, self).get_js_model_data()

        data_string = ''

        with self.obj.file as f:
            try:
                f.open()
                data_string = f.read()
            except (ValueError, IOError) as e:
                logging.error('Failed to read from file %s: %s',
                              self.obj.pk, e)

        data['xmlContent'] = pygments.highlight(
            force_unicode(data_string),
            pygments.lexers.XmlLexer(),
            pygments.formatters.HtmlFormatter())

        return data
