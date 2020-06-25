"""Admin URL definitions for the rbslack package."""

from __future__ import unicode_literals

from django.conf.urls import url
from reviewboard.extensions.views import configure_extension

from rbslack.extension import SlackExtension
from rbslack.forms import SlackSettingsForm


urlpatterns = [
    url(r'^$', configure_extension, {
        'ext_class': SlackExtension,
        'form_class': SlackSettingsForm,
    }),
]
