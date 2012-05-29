from django.conf.urls.defaults import patterns

from rbwebhooks.extension import RBWebHooksExtension
from rbwebhooks.forms import WebHooksSettingsForm


urlpatterns = patterns('',
    (r'^$', 'reviewboard.extensions.views.configure_extension',
     {'ext_class': RBWebHooksExtension,
      'form_class': WebHooksSettingsForm,
     }),
)
