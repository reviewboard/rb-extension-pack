"""URLs for the comment type extension."""

from django.urls import path
from reviewboard.extensions.views import configure_extension

from rbcommenttype.extension import CommentTypeExtension
from rbcommenttype.forms import CommentTypeSettingsForm


urlpatterns = [
    path(
        '',
        configure_extension,
        {
            'ext_class': CommentTypeExtension,
            'form_class': CommentTypeSettingsForm,
        },
        name='rbcommenttype-configure'),
]
