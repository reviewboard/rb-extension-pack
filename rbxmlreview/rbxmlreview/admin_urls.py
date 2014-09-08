from django.conf.urls import patterns, url


urlpatterns = patterns('rbxmlreview.views',
    url(r'^$', 'configure'),
)
