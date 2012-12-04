# rbxmlreview Extension for Review Board.
from mimetypes import XMLMimetype
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import ReviewUIHook, \
                                         FileAttachmentThumbnailHook, \
                                         URLHook

from rbxmlreview import XMLReviewUI


class XMLReviewUIExtension(Extension):
    def __init__(self, *args, **kwargs):
        super(XMLReviewUIExtension, self).__init__(*args, **kwargs)
        self.reviewui_hook = ReviewUIHook(self, [XMLReviewUI])
        self.thumbnail_hook = FileAttachmentThumbnailHook(self, [XMLMimetype])
