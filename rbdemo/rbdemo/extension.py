from __future__ import unicode_literals

from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import AuthBackendHook

from rbdemo.auth_backends import DemoAuthBackend


class DemoExtension(Extension):
    metadata = {
        'Name': 'Demo Server Extension',
        'Summary': 'Provides authentication and management for the '
                   'demo server.',
    }

    default_settings = {
        'auth_user_prefix': 'guest',
        'auth_user_max_id': 10000,
        'auth_password': 'demo',
        'auth_default_groups': [],
    }

    def initialize(self):
        AuthBackendHook(self, DemoAuthBackend)
