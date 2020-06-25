"""Message of the day extension for Review Board."""

from __future__ import unicode_literals

from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import TemplateHook


class MotdTemplateHook(TemplateHook):
    """Template hook to inject the motd."""

    def __init__(self, extension):
        """Initialize the hook.

        Args:
            extension (MotdExtension):
                The extension that owns the hook.
        """
        super(MotdTemplateHook, self).__init__(extension, 'base-after-navbar',
                                               'rbmotd/motd.html')

    def render_to_string(self, request, context):
        """Render the data for the hook location.

        Args:
            request (django.http.HttpRequest):
                The request object.

            context (dict):
                The template render context.

        Returns:
            django.utils.safestring.SafeText:
            The rendered HTML.
        """
        ext_settings = self.extension.settings

        context.update({
            'motd_close_value': '%s-closed' % ext_settings['message_id'],
            'motd_cookie': 'rbmotd',
            'motd_enabled': ext_settings.get('enabled'),
            'motd_message': ext_settings.get('message'),
        })

        return super(MotdTemplateHook, self).render_to_string(request, context)


class MotdExtension(Extension):
    """Extends Review Board to display a Message of the Day.

    This allows an administrator to set announcement text that will appear at
    the top of every page. This can be used for important announcements,
    status updates, downtime notices, or anything else.
    """
    metadata = {
        'Name': 'Message of the Day',
        'Summary': (
            'Displays a configurable, dismissable announcement or message '
            'that will be shown to all Review Board users.'
        ),
    }

    css_bundles = {
        'default': {
            'source_filenames': ['css/motd.less'],
        }
    }

    default_settings = {
        'enabled': False,
        'message': '',
        'message_id': '',
    }

    is_configurable = True

    def initialize(self):
        """Initialize the extension."""
        MotdTemplateHook(self)
