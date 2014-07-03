# reviewboard-together Extension for Review Board.
from django.conf import settings
from django.conf.urls import patterns, include
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import HeaderActionHook, HeaderDropdownActionHook, TemplateHook

class ReviewTogether(Extension):
    def __init__(self, *args, **kwargs):
        super(ReviewTogether, self).__init__(*args, **kwargs)
        self.script_injection = TemplateHook(self, "base-scripts-post",
            template_name="review_together/base.html")
        self.button = HeaderActionHook(self, [{
          "id": "launch-together",
          "label": "Chat",
          "url": "#"
        }]);

