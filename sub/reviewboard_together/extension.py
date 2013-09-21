# reviewboard-together Extension for Review Board.
from django.conf import settings
from django.conf.urls.defaults import patterns, include
from reviewboard.extensions.base import Extension

class ReviewBoardTogether(Extension):
    def __init__(self, *args, **kwargs):
        super(ReviewBoardTogether, self).__init__(*args, **kwargs)
