# reviewboard-together Extension for Review Board.
from reviewboard.extensions.base import Extension, JSExtension
from reviewboard.extensions.hooks import HeaderActionHook


class ReviewTogetherJSExtension(JSExtension):
    model_class = 'ReviewTogetherJS.Extension'


class ReviewTogether(Extension):
    default_settings = {
        'hub_url': '',
    }

    # This adds Review Board specific styling of the TogetherJS extension.
    css_bundles = {
        'default': {
            'source_filenames': ['css/review-together.less'],
        },
    }

    # This adds the required javascript files for the TogetherJS extension.
    js_bundles = {
        'default': {
            'source_filenames': ['js/togetherjs.js',
                                 'js/review-together.js'],
        },
    }

    is_configurable = True

    js_extensions = [ReviewTogetherJSExtension]

    def __init__(self, *args, **kwargs):
        super(ReviewTogether, self).__init__(*args, **kwargs)
        self.button = HeaderActionHook(self, [{
            "id": "launch-together",
            "label": "Chat",
            "url": "#",
        }])
