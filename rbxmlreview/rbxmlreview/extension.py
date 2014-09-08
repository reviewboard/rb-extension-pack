# rbxmlreview Extension for Review Board.
from mimetypes import XMLMimetype
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import (ReviewUIHook,
                                          FileAttachmentThumbnailHook)

from rbxmlreview import XMLReviewUI


class XMLReviewUIExtension(Extension):
    def initialize(self):
        ReviewUIHook(self, [XMLReviewUI])
        FileAttachmentThumbnailHook(self, [XMLMimetype])
