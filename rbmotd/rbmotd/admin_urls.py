"""Admin site URL definitions for the rbmotd extension."""

from __future__ import unicode_literals

from django.conf.urls import url
from reviewboard.extensions.views import configure_extension

from rbmotd.extension import MotdExtension
from rbmotd.forms import MotdSettingsForm


urlpatterns = [
    url(r'^$', configure_extension, {
         'ext_class': MotdExtension,
         'form_class': MotdSettingsForm,
     }),
]
