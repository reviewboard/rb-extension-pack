"""Admin site URL definitions for the rbmotd extension."""

from django.urls import path
from reviewboard.extensions.views import configure_extension

from rbmotd.extension import MotdExtension
from rbmotd.forms import MotdSettingsForm


urlpatterns = [
    path(
        '',
        configure_extension,
        {
             'ext_class': MotdExtension,
             'form_class': MotdSettingsForm,
        }),
]
