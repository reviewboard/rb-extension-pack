from django.conf.urls import patterns, url

from review_together.extension import ReviewTogether
from review_together.forms import ReviewTogetherSettingsForm


urlpatterns = patterns(
    '',
    url(r'^$',
        'reviewboard.extensions.views.configure_extension',
        {
            'ext_class': ReviewTogether,
            'form_class': ReviewTogetherSettingsForm,
        }),
)
