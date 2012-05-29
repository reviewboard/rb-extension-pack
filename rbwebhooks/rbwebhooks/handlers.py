from django.utils.translation import ugettext as _

from reviewboard.reviews.signals import review_request_published


class SignalHandlers(object):
    """
    Signal handlers for reviewboard signals

    Each signal handler should be defined here and connected in __init__
    """
    # This attribute is also used by the admin panel when specifying
    # Web Hook Targets. The convention followed is to name each
    # choice as the signal which is caught to detect the event.
    HOOK_CHOICES = (
        ('review_request_published', _("Review Request published")),
    )

    def __init__(self, extension):
        """Initialize and connect all the signals"""
        self.extension = extension

        # Connect the handlers.
        review_request_published.connect(self._review_request_published)

    def _review_request_published(self, **kwargs):
        review_request = kwargs.get('review_request')
        review_request_id = review_request.get_display_id()

        # Get the changes from the change description. The change description
        # is only None when this is a new review request, and not an update.
        changedesc = kwargs.get('changedesc')
        fields_changed = {}
        is_new = changedesc is None

        if not is_new:
            fields_changed = changedesc.fields_changed

        request_args = {
            'review_request_id': review_request_id,
            'new': is_new,
            'fields_changed': fields_changed,
        }
        self.extension.notify('review_request_published', request_args)
