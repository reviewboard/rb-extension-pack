from __future__ import unicode_literals

from django.conf.urls import patterns

from rbslack.extension import SlackExtension
from rbslack.forms import SlackSettingsForm


urlpatterns = patterns(
    '',
    (r'^$', 'reviewboard.extensions.views.configure_extension', {
        'ext_class': SlackExtension,
        'form_class': SlackSettingsForm,
     }),
)
