"""rbwebhooks extension for Review Board.

This extension allows remote services to be notified of events occuring
within Review Board. An administrator may add "Target" URLs, at which
the extension will fire HTTP POST requests when the specified hook
event occurs.
"""

from __future__ import unicode_literals

import json
import logging

from django.utils.six.moves.urllib.error import URLError
from django.utils.six.moves.urllib.parse import urlencode
from django.utils.six.moves.urllib.request import Request, urlopen
from reviewboard.extensions.base import Extension

from rbwebhooks.handlers import SignalHandlers
from rbwebhooks.models import WebHookTarget


class RBWebHooksExtension(Extension):
    """A Web Hooks Extension for Review Board"""

    is_configurable = True
    has_admin_site = True
    default_settings = {
        'attempts': 1,
    }

    def initialize(self):
        """Initialize the extension."""
        self.settings.load()
        self.signal_handlers = SignalHandlers(self)

    def notify(self, hook_id, request_payload):
        """Notify webhooks corresponding to a specific hook_id.

        Args:
            hook_id (unicode):
                The ID of the hook to notify.

            request_payload (object):
                The payload to send. This will get encoded as JSON.
        """
        targets = WebHookTarget.objects.filter(
            hook_id=hook_id,
            enabled=True,
        )

        payload = json.dumps(request_payload)
        attempts = self.settings['attempts']

        for target in targets:
            self._send_web_request(target.url, payload, attempts)

    def _send_web_request(self, url, payload, attempts=1):
        """Send out a web request and retry on failure.

        TODO: Currently this is a blocking operation. Devising a way to send
        these requests without blocking would be benificial.

        Args:
            url (unicode):
                The URL to send the request to.

            payload (unicode):
                The JSON-encoded payload to send.

            attempts (int):
                The number of retry attempts left.
        """
        request = Request(url)
        arguments = urlencode({
            'payload': payload,
        })
        # The addition of data automatically converts request to a POST.
        request.add_data(arguments)

        while attempts:
            try:
                return urlopen(request)
            except URLError:
                attempts -= 1

        logging.warning('Sending WebHook Request failed: %s ' % url)
