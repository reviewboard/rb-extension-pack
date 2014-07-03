from django.conf.urls import patterns, url

from review_together.extension import ReviewTogether


urlpatterns = patterns('review_together.views',
    url(r'^$', 'configure'),
)
