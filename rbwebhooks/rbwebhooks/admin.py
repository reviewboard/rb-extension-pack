from django.contrib import admin

from reviewboard.extensions.base import get_extension_manager

from rbwebhooks.extension import RBWebHooksExtension
from rbwebhooks.models import WebHookTarget


class WebHookTargetAdmin(admin.ModelAdmin):
    fields = ['hook_id', 'url', 'description', 'enabled']
    list_display = ('hook_id', 'url', 'enabled')
    list_filter = ('enabled', 'hook_id')
    actions = ['make_enabled', 'make_disabled']

    def make_enabled(self, request, queryset):
        queryset.update(enabled=True)
    make_enabled.short_description = "Enable selected targets"

    def make_disabled(self, request, queryset):
        queryset.update(enabled=False)
    make_disabled.short_description = "Disable selected targets"


# Get the RBWebHooksExtension instance. We can assume it exists because
# this code is executed after the extension has been registered with
# the manager.
extension_manager = get_extension_manager()
extension = extension_manager.get_enabled_extension(RBWebHooksExtension.id)

# Register with the extension's, not Review Board's, admin site.
extension.admin_site.register(WebHookTarget, WebHookTargetAdmin)
