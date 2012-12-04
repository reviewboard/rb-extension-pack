from django.conf.urls.defaults import patterns, url

from rbxmlreview.extension import XMLReviewUIExtension


urlpatterns = patterns('rbxmlreview.views',
    url(r'^$', 'configure'),
)
