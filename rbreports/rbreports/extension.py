# Reports extension for Review Board.
from django.conf import settings
from django.conf.urls.defaults import patterns, include
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import DashboardHook, URLHook


class ReportsDashboardHook(DashboardHook):
    def get_entries(self):
        return [{
            'label': 'Reports',
            'url': settings.SITE_ROOT + 'reports/',
        }]


class ReportsExtension(Extension):
    is_configurable = True

    def __init__(self):
        Extension.__init__(self)

        self.url_hook = URLHook(self, patterns('',
            (r'^reports/', include('rbreports.urls'))))

        self.dashboard_hook = ReportsDashboardHook(self)
