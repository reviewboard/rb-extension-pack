from __future__ import unicode_literals

import time

from django.utils import six
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import UserInfoboxHook
from reviewboard.reviews.models import ReviewRequest


class UserStatsInfoboxHook(UserInfoboxHook):
    """Add user statistics to the infobox."""

    def get_etag_data(self, user, request, local_site):
        """Return data to include in the ETag calculation.

        When this extension is enabled, we don't want the browser to cache
        anything, because we don't save any work by doing so. Just return a
        cache-busting timestamp.

        Args:
            user (django.contrib.auth.models.User):
                The user whose infobox is being shown.

            request (django.http.HttpRequest):
                The request object.

            local_site (reviewboard.site.models.LocalSite):
                The current local site, if any.

        Returns:
            six.text_type:
            Data to include in the ETag.
        """
        return six.text_type(time.time())

    def get_extra_context(self, user, request, local_site):
        """Return context to include when rendering the template.

        Args:
            user (django.contrib.auth.models.User):
                The user whose infobox is being shown.

            request (django.http.HttpRequest):
                The request object.

            local_site (reviewboard.site.models.LocalSite):
                The current local site, if any.

        Returns:
            dict:
            Additional data to include when rendering the template.
        """
        return {
            'incoming': ReviewRequest.objects.to_user(
                user, user=request.user, local_site=local_site).count(),
            'outgoing': ReviewRequest.objects.from_user(
                user, user=request.user, local_site=local_site).count(),
        }


class RBUserStats(Extension):
    """The user statistics extension."""

    metadata = {
        'Name': 'rb-user-stats',
        'Summary': 'Show statistics for Review Board users in the infobox',
    }

    def initialize(self):
        """Initialize the extension."""
        UserStatsInfoboxHook(self, 'rb-user-stats-infobox.html')
