from django.utils.encoding import force_unicode
import pygments

from reviewboard.attachments.mimetypes import TextMimetype


class XMLMimetype(TextMimetype):
    """This handles XML (.xml) mimetypes."""
    supported_mimetypes = ['application/xml', 'text/xml']

    def _generate_preview_html(self, data_string):
        """Returns syntax-highlighted XML."""
        return pygments.highlight(
            force_unicode(data_string),
            pygments.lexers.XmlLexer(),
            pygments.formatters.HtmlFormatter())
