from __future__ import unicode_literals

from reviewboard.extensions.base import Extension, JSExtension
from reviewboard.extensions.hooks import TemplateHook
from reviewboard.urls import reviewable_url_names, review_request_url_names


_apply_to_url_names = set(reviewable_url_names + review_request_url_names)


class StopwatchJSExtension(JSExtension):
    """Javascript extension for the stopwatch."""

    model_class = 'RBStopwatch.Extension'
    apply_to = _apply_to_url_names


class StopwatchExtension(Extension):
    """A stopwatch extension.

    This extension adds a bit of UI to every review request page that gives
    reviewers a "stopwatch" which allows them to turn on and off a timer. The
    total time spent reviewing will be added to the Review's extra_data.
    """

    metadata = {
        'Name': 'Review Stopwatch',
        'Summary': 'A stopwatch for reviewers: keep track of the total time '
                   'spent on each code review.',
    }

    js_extensions = [StopwatchJSExtension]

    css_bundles = {
        'default': {
            'source_filenames': ['css/stopwatch.less'],
            'apply_to': _apply_to_url_names,
        },
    }

    js_bundles = {
        'default': {
            'source_filenames': ['js/stopwatch.js'],
            'apply_to': _apply_to_url_names,
        },
    }

    def initialize(self):
        """Initialize the extension."""
        TemplateHook(self, 'review-summary-header-post',
                     'rbstopwatch-review-header.html',
                     apply_to=['review-request-detail'])
