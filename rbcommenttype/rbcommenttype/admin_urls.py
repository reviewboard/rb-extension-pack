from __future__ import unicode_literals

from django.conf.urls import url

from rbcommenttype.extension import CommentTypeExtension
from rbcommenttype.forms import CommentTypeSettingsForm

from reviewboard.extensions.views import configure_extension


urlpatterns = [
    url('^$',
        configure_extension,
        {
            'ext_class': CommentTypeExtension,
            'form_class': CommentTypeSettingsForm,
        },
        name='rbcommenttype-configure'),
]
