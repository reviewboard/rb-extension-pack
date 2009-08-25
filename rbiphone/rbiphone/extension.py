# iPhone extension for Review Board.
from django.conf import settings
from django.conf.urls.defaults import patterns, include
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import URLHook
from djblets.extensions.hooks import TemplateHook


class IPhoneExtension(Extension):
    def __init__(self):
        Extension.__init__(self)

        URLHook(self, patterns('', (r'^iphone/', include('rbiphone.urls'))))
        TemplateHook(self, "base-after-navbar", "rbiphone/iphone_link.html")
