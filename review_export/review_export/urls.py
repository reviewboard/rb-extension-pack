from django.conf.urls import patterns, url


urlpatterns = patterns(
    'review_export.views',
    url(r'pdf/(?P<review_request_id>[0-9]+)/$', 'send_pdf_file'),
    url(r'xml/(?P<review_request_id>[0-9]+)/$', 'send_xml_file'),
)
