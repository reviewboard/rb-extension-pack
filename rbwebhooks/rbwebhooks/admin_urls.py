"""Admin URLs for the rbwebhooks extension."""

from __future__ import unicode_literals

from django.conf.urls import url
from reviewboard.extensions.views import configure_extension

from rbwebhooks.extension import RBWebHooksExtension
from rbwebhooks.forms import WebHooksSettingsForm


urlpatterns = [
    url(r'^$', configure_extension, {
        'ext_class': RBWebHooksExtension,
        'form_class': WebHooksSettingsForm,
    }),
]
