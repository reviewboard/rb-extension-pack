"""Admin URL definitions for the Review Together extension."""

from django.conf.urls import url
from reviewboard.extensions.views import configure_extension

from review_together.extension import ReviewTogether
from review_together.forms import ReviewTogetherSettingsForm


urlpatterns = [
    url(r'^$', configure_extension,
        {
            'ext_class': ReviewTogether,
            'form_class': ReviewTogetherSettingsForm,
        }),
]
