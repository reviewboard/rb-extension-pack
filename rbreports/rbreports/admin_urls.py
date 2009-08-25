from django.conf.urls.defaults import patterns, include


urlpatterns = patterns('',
    (r'^$', 'rbreports.views.configure')
)
