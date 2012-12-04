import logging

from django.utils.encoding import force_unicode
from reviewboard.reviews.ui.base import FileAttachmentReviewUI
import pygments


class XMLReviewUI(FileAttachmentReviewUI):
    """This is a ReviewUI for XML mimetypes."""
    supported_mimetypes = ['application/xml', 'text/xml']
    template_name = 'rbxmlreview/xml.html'
    object_key = 'xml'

    def render(self):
        """Returns syntax-highlighted XML as HTML."""
        data_string = ""
        f = self.obj.file

        try:
            f.open()
            data_string = f.read()
        except (ValueError, IOError), e:
            logging.error('Failed to read from file %s: %s' % (self.obj.pk, e))

        f.close()

        return pygments.highlight(
            force_unicode(data_string),
            pygments.lexers.XmlLexer(),
            pygments.formatters.HtmlFormatter())
