# shipit_ascii_art Extension for Review Board.
from django.conf import settings
from django.conf.urls.defaults import patterns, include
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import DashboardHook, URLHook

from shipit_ascii_art.handlers import SignalHandlers


class AsciiArtURLHook(URLHook):
    def __init__(self, extension, *args, **kwargs):
        pattern = patterns('', (r'^shipit_ascii_art/',
                            include('shipit_ascii_art.urls')))
        super(AsciiArtURLHook, self).__init__(extension, pattern)


class AsciiArtDashboardHook(DashboardHook):
    def __init__(self, extension, *args, **kwargs):
        entries = [{
            'label': 'Ship It Ascii Art',
            'url': settings.SITE_ROOT + 'shipit_ascii_art/',
        }]
        super(AsciiArtDashboardHook, self).__init__(extension,
                entries=entries, *args, **kwargs)

class AsciiArt(Extension):
    is_configurable = True
    def __init__(self, *args, **kwargs):
        super(AsciiArt, self).__init__(*args, **kwargs)
        self.url_hook = AsciiArtURLHook(self)
        self.dashboard_hook = AsciiArtDashboardHook(self)
        self.signal_handlers = SignalHandlers(self)
        # This variable will be changed or refactored when
        # Ascii art is made configurable
        self.ascii_pattern = "basic"
