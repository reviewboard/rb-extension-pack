from django.conf.urls.defaults import patterns, url

from shipit_ascii_art.extension import AsciiArt


urlpatterns = patterns('shipit_ascii_art.views',
    url(r'^$', 'configure'),
)
