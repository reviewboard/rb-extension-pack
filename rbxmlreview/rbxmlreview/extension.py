"""XML review extension for Review Board."""

from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import (ReviewUIHook,
                                          FileAttachmentThumbnailHook)

from rbxmlreview.mimetypes import XMLMimetype
from rbxmlreview.reviewui import XMLReviewUI


class XMLReviewUIExtension(Extension):
    """XML Review extension for Review Board"""

    js_bundles = {
        'xmlreviewable': {
            'source_filenames': (
                'js/xmlReviewableModel.es6.js',
                'js/xmlReviewableView.es6.js',
            ),
        },
    }

    def initialize(self):
        """Initialize the extension."""
        ReviewUIHook(self, [XMLReviewUI])
        FileAttachmentThumbnailHook(self, [XMLMimetype])
