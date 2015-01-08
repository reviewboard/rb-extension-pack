from django.conf.urls import include, patterns, url

from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import URLHook

from review_export.hooks import ReviewRequestDropdownActionHookWithDynamicUrl


class ReviewExport(Extension):
    """Allows users to export a review request to XML/PDF.

    Review Export is an extension for Review Board that allows a user to
    download a file representative of a review request.
    """
    def __init__(self, *args, **kwargs):
        # A dropdown list in the review request menu toolbar
        super(ReviewExport, self).__init__(*args, **kwargs)
        ReviewRequestDropdownActionHookWithDynamicUrl(self, [
            {
                'label': 'Export',
                'items': [
                    {
                        'id': 'export-pdf',
                        'label': 'as PDF',
                        'url': '/review_export/pdf/%s',
                    },
                    {
                        'id': 'export-xml',
                        'label': 'as XML',
                        'url': '/review_export/xml/%s',
                    },
                ],
            },
        ])

        patterns(
            '',
            url(r'^review_export/', include('review_export.urls'))
        )
        URLHook(self, patterns('',
                               url(r'review_export/',
                                   include('review_export.urls'))))
