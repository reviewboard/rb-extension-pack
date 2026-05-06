"""Message of the day extension for Review Board."""

from __future__ import annotations

from typing import TYPE_CHECKING

import reviewboard
from django.utils.safestring import mark_safe
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import TemplateHook

if TYPE_CHECKING:
    from typing import Any

    from django.http import HttpRequest
    from django.template import Context
    from django.utils.safestring import SafeString


class LegacyMotdTemplateHook(TemplateHook):
    """Template hook for displaying a legacy Message of the Day banner.

    This displays the banner in the navigation area, handling the styling
    and interaction.

    This is a legacy banner used in Review Board 7.0 and earlier.

    Version Added:
        4.0:
        This was the original template hook, named ``MotdTemplateHook``.
    """

    def __init__(
        self,
        extension: MotdExtension,
    ) -> None:
        """Initialize the hook.

        Args:
            extension (MotdExtension):
                The extension that owns the hook.
        """
        super().__init__(extension, 'base-after-navbar', 'rbmotd/motd.html')

    def render_to_string(
        self,
        request: HttpRequest,
        context: Context,
    ) -> SafeString:
        """Render the data for the hook location.

        Args:
            request (django.http.HttpRequest):
                The request object.

            context (dict):
                The template render context.

        Returns:
            django.utils.safestring.SafeString:
            The rendered HTML.
        """
        ext_settings = self.extension.settings
        message_id = ext_settings['message_id']

        context.update({
            'banner_can_close': ext_settings.get('can_close', True),
            'banner_id': 'motd',
            'motd_close_value': f'{message_id}-closed',
            'motd_cookie': 'rbmotd',
            'motd_enabled': ext_settings.get('enabled'),
            'motd_message': ext_settings.get('message'),
        })

        return super().render_to_string(request, context)


class MotdPageBannerTemplateHook(TemplateHook):
    """Template hook for displaying a Message of the Day page banner.

    This utilizes the page banner support in Review Board 8.0+, displaying
    the Message of the Day using a standard layout and presentation.

    Version Added:
        4.0
    """

    name = 'page-banners'
    template_name = 'ui/components/page-banner.html'

    def should_render(
        self,
        *,
        request: HttpRequest,
        context: Context,
    ) -> bool:
        """Return whether the banner should be rendered.

        If the banner is not enabled, or the user has a cookie set indicating
        they closed the banner, the banner will not be rendered.

        Args:
            request (django.http.HttpRequest):
                The HTTP request from the client.

            context (django.template.Context):
                The context data for the template.

        Returns:
            bool:
            ``True`` if the banner is enabled and has not been closed.
            ``False`` otherwise.
        """
        return (
            context['motd_enabled'] and
            context['banner_header'] and
            (request.COOKIES.get(context['motd_cookie']) !=
             context['motd_close_value'])
        )

    def get_extra_context(
        self,
        request: HttpRequest,
        context: Context,
    ) -> dict[str, Any]:
        """Return extra context data for the template.

        This will include state for the Page Banner component, plus
        state for handling the interactivity and visibility of the banner.

        Args:
            request (django.http.HttpRequest):
                The HTTP request from the client.

            context (django.template.Context):
                The context data for the template.

        Returns:
            dict:
            Context data for the template.
        """
        ext_settings = self.extension.settings
        message_id = ext_settings['message_id']

        return {
            'banner_can_close': ext_settings.get('can_close', True),
            'banner_header': mark_safe(ext_settings.get('message')),
            'banner_id': 'motd-banner',
            'banner_scripts_template_name': 'rbmotd/scripts.html',
            'motd_close_value': f'{message_id}-closed',
            'motd_cookie': 'rbmotd',
            'motd_enabled': ext_settings.get('enabled'),
        }


class MotdExtension(Extension):
    """Extends Review Board to display a Message of the Day.

    This allows an administrator to set announcement text that will appear at
    the top of every page. This can be used for important announcements,
    status updates, downtime notices, or anything else.

    Version Changed:
        4.0:
        * Review Board 8.0+ page banners are now supported.
        * Administrators can now control whether banners can be closed.
    """

    metadata = {
        'Name': 'Message of the Day',
        'Summary': (
            'Displays a configurable, dismissable announcement or message '
            'that will be shown to all Review Board users.'
        ),
    }

    # NOTE: CSS bundles can be removed when Review Board 8.0 is the minimum
    #       requirement.
    css_bundles = {
        'default': {
            'source_filenames': ['css/motd.less'],
        }
    }

    default_settings = {
        'can_close': True,
        'enabled': False,
        'message': '',
        'message_id': '',
    }

    is_configurable = True

    def initialize(self) -> None:
        """Initialize the extension."""
        if reviewboard.VERSION[:2] >= (7, 1):
            MotdPageBannerTemplateHook(self)
        else:
            LegacyMotdTemplateHook(self)
