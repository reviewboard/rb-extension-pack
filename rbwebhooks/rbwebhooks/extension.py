# rbwebhooks extension for Review Board.
#
# This extension allows remote services to be notified of events occuring
# within Review Board. An administrator may add "Target" URLs, at which
# the extension will fire HTTP POST requests when the specified hook
# event occurs.
import json
import logging

import requests
from requests.exceptions import RequestException

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

    def __init__(self, *args, **kwargs):
        super(RBWebHooksExtension, self).__init__(*args, **kwargs)
        self.settings.load()
        self.signal_handlers = SignalHandlers(self)

    def notify(self, hook_id, request_payload):
        """
        Make web requests corresponding to a specific hook_id

        Called by signal handlers to send the web requests
        """
        targets = WebHookTarget.objects.filter(
            hook_id=hook_id,
            enabled=True,
        )

        for target in targets:
            self._send_web_request(
                hook_id,
                target.url,
                request_payload,
                self.settings['attempts'])

    def _send_web_request(self, hook_id, url, request_payload, attempts=1):
        """
        Send out a web request and retry on failure.

        Currently this is a blocking operation. devising a way to send
        these requests without blocking would be bennificial.
        """
        logging.info("Sending WebHook request: %s %s" % (hook_id, request_payload))

        auth = None
        username = self.settings['username']
        password = self.settings['password']
        if username and password:
            auth = (username, password)

        headers = {'X-ReviewBoard-Event': hook_id}
        data = self._encode_payload(request_payload)

        err = None
        while attempts:
            try:
                return requests.post(url, auth=auth, headers=headers, data=data)
            except RequestException as ex:
                attempts -= 1
                err = ex

        logging.warning("Sending WebHook request failed: %s [%s]" % (url, err))
        return None

    def _encode_payload(self, request_payload):
        return json.dumps(request_payload)
