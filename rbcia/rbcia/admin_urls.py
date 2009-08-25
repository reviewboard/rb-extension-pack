from django.conf.urls.defaults import patterns

from rbcia.extension import CIAExtension
from rbcia.forms import CIASettingsForm


urlpatterns = patterns('',
    (r'^$', 'reviewboard.extensions.views.configure_extension',
     {'ext_class': CIAExtension,
      'form_class': CIASettingsForm,
    })
)
