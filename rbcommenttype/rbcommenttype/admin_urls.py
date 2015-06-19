from __future__ import unicode_literals

from django.conf.urls import patterns, url

from rbcommenttype.extension import CommentTypeExtension
from rbcommenttype.forms import CommentTypeSettingsForm


urlpatterns = patterns(
    '',

    url('^$',
        'reviewboard.extensions.views.configure_extension',
        {
            'ext_class': CommentTypeExtension,
            'form_class': CommentTypeSettingsForm,
        },
        name='rbcommenttype-configure'),
)
