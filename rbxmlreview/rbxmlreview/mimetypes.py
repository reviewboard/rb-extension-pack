"""XML Mimetype definition."""

import pygments

from reviewboard.attachments.mimetypes import TextMimetype


class XMLMimetype(TextMimetype):
    """This handles XML (.xml) mimetypes."""

    supported_mimetypes = ['application/xml', 'text/xml']

    def _generate_preview_html(self, data_string):
        """Return syntax-highlighted XML.

        Args:
            data_string (str):
                The XML data.

        Returns:
            str:
            The HTML-formatted rendered string.
        """
        if isinstance(data_string, bytes):
            data_string = data_string.decode('utf-8')

        return pygments.highlight(
            data_string,
            pygments.lexers.XmlLexer(),
            pygments.formatters.HtmlFormatter())
