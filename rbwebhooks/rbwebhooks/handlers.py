from django.utils.translation import ugettext as _

import reviewboard.settings as settings
from reviewboard.reviews.signals import (review_request_published,
                                         review_request_closed,
                                         review_request_reopened,
                                         review_published)


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
        ('review_request_closed', _("Review Request closed")),
        ('review_request_reopened', _("Review Request reopened")),
        ('review_request_approved', _("Review Request approved")),
    )

    def __init__(self, extension):
        """Initialize and connect all the signals"""
        self.extension = extension

        # Connect the handlers.
        review_request_published.connect(self._review_request_published)
        review_request_closed.connect(self._review_request_closed)
        review_request_reopened.connect(self._review_request_reopened)
        review_published.connect(self._review_published)

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

        user = kwargs.get('user')
        if user.is_authenticated:
            request_args['user'] = user.username

        self.extension.notify('review_request_published', request_args)

    def _review_request_closed(self, **kwargs):
        rr = kwargs.get('review_request')
        request_args = {
            'review_request_id': rr.get_display_id(),
            'type': kwargs.get('type'),
        }

        user = kwargs.get('user')
        if user.is_authenticated:
            request_args['user'] = user.username

        self.extension.notify('review_request_closed', request_args)

    def _review_request_reopened(self, **kwargs):
        rr = kwargs.get('review_request')
        request_args = {
            'review_request_id': rr.get_display_id(),
        }

        user = kwargs.get('user')
        if user.is_authenticated:
            request_args['user'] = user.username

        self.extension.notify('review_request_reopened', request_args)

    def _review_published(self, **kwargs):
        r = kwargs.get('review')
        if not r.ship_it:
            return

        request_args = {
            'review_request_id': r.review_request.get_display_id(),
        }

        user = kwargs.get('user')
        if user.is_authenticated:
            request_args['user'] = user.username

        self.extension.notify('review_request_approved', request_args)
