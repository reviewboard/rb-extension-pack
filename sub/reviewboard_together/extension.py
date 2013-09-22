# reviewboard-together Extension for Review Board.
from django.conf import settings
from django.conf.urls.defaults import patterns, include
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import HeaderActionHook, HeaderDropdownActionHook, TemplateHook

class ReviewBoardTogether(Extension):
    def __init__(self, *args, **kwargs):
        super(ReviewBoardTogether, self).__init__(*args, **kwargs)
        self.script_injection = TemplateHook(self, "base-scripts-post",
            template_name="reviewboard_together/base.html")
        self.button = HeaderActionHook(self, [{
          "id": "launch-together",
          "label": "TogetherJS",
          "url": "#"
        }]);

