"""Review Together extension for Review Board."""

from reviewboard.extensions.base import Extension, JSExtension
from reviewboard.extensions.hooks import HeaderActionHook


class ReviewTogetherJSExtension(JSExtension):
    """JavaScript extension for Review Together."""

    model_class = 'ReviewTogetherJS.Extension'


class ReviewTogether(Extension):
    """Review Board extension for Review Together."""

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
                                 'js/reviewTogether.es6.js'],
        },
    }

    is_configurable = True
    js_extensions = [ReviewTogetherJSExtension]

    def __init__(self, *args, **kwargs):
        """Initialize the extension.

        Args:
            *args (tuple):
                Positional arguments to pass through to the superclass.

            **kwargs (dict):
                Keyword arguments to pass through to the superclass.
        """
        super(ReviewTogether, self).__init__(*args, **kwargs)
        self.button = HeaderActionHook(self, [{
            'id': 'launch-together',
            'label': 'Chat',
            'url': '#',
        }])
