# reviewboard-together Extension for Review Board.
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import HeaderActionHook, TemplateHook

class ReviewTogether(Extension):
    # This adds reviewboard specific styling of the TogetherJS extension.
    css_bundles = {
        'default': {
            'source_filenames': ['css/review-together.less'],
        },
    }

    def __init__(self, *args, **kwargs):
        super(ReviewTogether, self).__init__(*args, **kwargs)
        self.script_injection = TemplateHook(
            self, "base-scripts-post",
            template_name="review_together/base.html")
        self.button = HeaderActionHook(self, [{
            "id": "launch-together",
            "label": "Chat",
            "url": "#"
        }]);
