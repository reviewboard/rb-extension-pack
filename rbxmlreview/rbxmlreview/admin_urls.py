from django.conf.urls import patterns, url

from rbxmlreview.extension import XMLReviewUIExtension


urlpatterns = patterns('rbxmlreview.views',
    url(r'^$', 'configure'),
)
