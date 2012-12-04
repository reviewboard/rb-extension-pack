# Reports extension for Review Board.
from django.conf import settings
from django.conf.urls.defaults import patterns, include
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import DashboardHook, URLHook


class ReportsExtension(Extension):
    is_configurable = True

    def __init__(self, *args, **kwargs):
        super(ReportsExtension, self).__init__(*args, **kwargs)

        self.url_hook = URLHook(self, patterns('',
            (r'^reports/', include('rbreports.urls'))))

        self.dashboard_hook = DashboardHook(self, entries=[
            {
                'label': 'Reports',
                'url': settings.SITE_ROOT + 'reports/',
            }
        ])
