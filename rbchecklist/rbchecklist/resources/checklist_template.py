from django.core.exceptions import ObjectDoesNotExist
from djblets.webapi.decorators import webapi_request_fields
from djblets.webapi.errors import DOES_NOT_EXIST
from reviewboard.webapi.base import WebAPIResource
from reviewboard.webapi.decorators import (webapi_check_local_site,
                                           webapi_login_required,
                                           webapi_response_errors)

from rbchecklist.models import ChecklistTemplate


class ChecklistTemplateResource(WebAPIResource):
    """Provide information on checklist templates."""

    name = 'checklist_template'
    name_plural = 'checklist_templates'
    model = ChecklistTemplate
    uri_object_key = 'checklist_template_id'
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')

    fields = {
        'id': {
            'type': int,
            'description': 'Id of the checklist template.',
        },
        'title': {
            'type': str,
            'description': 'Title of the checklist template.',
        },
        'items': {
            'type': str,
            'description': 'Items in the checklist template.',
        },
    }

    def has_access_permissions(self, request, obj, *args, **kwargs):
        return request.user == obj.owner

    def has_modify_permissions(self, request, obj, *args, **kwargs):
        return request.user == obj.owner

    def has_delete_permissions(self, request, obj, *args, **kwargs):
        return request.user == obj.owner

    @webapi_login_required
    @webapi_request_fields(
        required={
            'title': {
                'type': str,
                'description': 'The title of the checklist template.',
            },
            'items': {
                'type': str,
                'description': 'JSON string of checklist items.',
            },
        },
    )
    @webapi_check_local_site
    def create(self, request, title=None, items=None, *args, **kwargs):
        """Create a new checklist template."""

        checklist_template = ChecklistTemplate.objects.create(
            title=title,
            owner=request.user,
            items=items
        )

        return 201, {
            self.item_result_key: checklist_template
        }

    @webapi_login_required
    @webapi_response_errors(DOES_NOT_EXIST)
    @webapi_request_fields(
        required={
            'title': {
                'type': str,
                'description': 'The title of the checklist template.',
            },
            'items': {
                'type': str,
                'description': 'JSON string of checklist items.',
            },
        },
    )
    @webapi_check_local_site
    def update(self, request, title=None, items=None, *args, **kwargs):
        """Update a checklist template."""

        try:
            checklist_template = self.get_object(request, args, **kwargs)
        except ObjectDoesNotExist:
            return DOES_NOT_EXIST

        if not self.has_modify_permissions(request, checklist_template):
            return self._no_access_error(request.user)

        checklist_template.title = title
        checklist_template.items = items
        checklist_template.save()

        checklist_template = ChecklistTemplate.objects.filter(
            pk=kwargs[self.uri_object_key]
        ).first()

        return 200, {
            self.item_result_key: checklist_template
        }

    def get_queryset(self, request, is_list=False, *args, **kwargs):
        """Return only checklist templates that belong to the user."""

        return self.model.objects.filter(owner=request.user)


checklist_template_resource = ChecklistTemplateResource()
