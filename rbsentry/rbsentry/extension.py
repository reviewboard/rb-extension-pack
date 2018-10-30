"""Sentry.io extension for Review Board."""

from __future__ import unicode_literals

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import TemplateHook

import sentry_sdk


class RbsentryExtension(Extension):
    """Error monitoring for Review Board using Sentry.io."""

    metadata = {
        'Name': _('Sentry.io integration'),
        'Summary': _('Error monitoring using Sentry.io'),
    }

    def initialize(self):
        """Initialize the extension."""
        if hasattr(settings, 'SENTRY'):
            sentry_sdk.init(
                settings.SENTRY['DSN'],
                environment=settings.SENTRY['ENVIRONMENT'])

            TemplateHook(self,
                         'base-scripts',
                         'sentry-js.html')
