from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('shipit_ascii_art.views',
    url(r'^$', 'configure'),
)
