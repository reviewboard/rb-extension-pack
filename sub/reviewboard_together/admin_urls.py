from django.conf.urls.defaults import patterns, url

from reviewboard_together.extension import ReviewBoardTogether


urlpatterns = patterns('reviewboard_together.views',
    url(r'^$', 'configure'),
)
