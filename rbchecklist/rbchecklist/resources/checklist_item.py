from __future__ import unicode_literals

from django.utils import six
from djblets.webapi.decorators import (webapi_login_required,
                                       webapi_response_errors,
                                       webapi_request_fields)
from djblets.webapi.errors import DOES_NOT_EXIST
from reviewboard.webapi.base import WebAPIResource
from reviewboard.webapi.decorators import webapi_check_local_site

from rbchecklist.models import ReviewChecklist as Checklist


class ChecklistItemResource(WebAPIResource):
    """Provide information for individual checklist items of a checklist."""

    name = 'checklist_item'
    uri_object_key = 'checklist_item_id'
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')

    fields = {
        'id': {
            'type': six.text_type,
            'description': 'The id of the checklist item.',
        },
        'description': {
            'type': six.text_type,
            'description': 'The description of the checklist item.',
        },
        'checked': {
            'type': bool,
            'description': 'Whether the checklist item is finished.',
        },
    }

    def get_parent_object(self, pk):
        """Return the parent checklist object."""
        return self._parent_resource.model.objects.get(pk=pk)

    @webapi_login_required
    @webapi_response_errors(DOES_NOT_EXIST)
    @webapi_check_local_site
    def get(self, request, api_format, checklist_id, checklist_item_id, *args,
            **kwargs):
        """Return the individual checklist item."""
        try:
            checklist = self.get_parent_object(checklist_id)
        except Checklist.ObjectDoesNotExist:
            return DOES_NOT_EXIST

        if six.text_type(checklist_item_id) not in checklist.checklist_items:
            return DOES_NOT_EXIST

        item = checklist.checklist_items.get(six.text_type(checklist_item_id))
        return 200, {self.item_result_key: item}

    @webapi_login_required
    @webapi_response_errors(DOES_NOT_EXIST)
    @webapi_check_local_site
    def get_list(self, request, api_format, checklist_id, *args, **kwargs):
        """Return a list of checklist items in the checklist specified."""
        try:
            checklist = self.get_parent_object(checklist_id)
        except Checklist.ObjectDoesNotExist:
            return DOES_NOT_EXIST

        return 200, {self.item_result_key: checklist.checklist_items}

    @webapi_request_fields(
        required={
            'description': {
                'type': six.text_type,
                'description': 'The description of the checklist item.',
            },
            'checked': {
                'type': bool,
                'description': 'Whether the item is checked.',
            },
        }
    )
    @webapi_login_required
    @webapi_response_errors(DOES_NOT_EXIST)
    @webapi_check_local_site
    def create(self, request, api_format, checklist_id, description=None,
               *args, **kwargs):
        """Add a new checklist item to the checklist."""
        try:
            checklist = self.get_parent_object(checklist_id)
        except Checklist.ObjectDoesNotExist:
            return DOES_NOT_EXIST

        item = checklist.add_item(description)
        return 201, {self.item_result_key: item}

    @webapi_request_fields(
        optional={
            'description': {
                'type': six.text_type,
                'description': 'The description of the checklist item.',
            },
            'checked': {
                'type': bool,
                'description': 'Whether the checklist item is completed.',
            },
        }
    )
    @webapi_login_required
    @webapi_response_errors(DOES_NOT_EXIST)
    @webapi_check_local_site
    def update(self, request, api_format, checklist_id, checklist_item_id,
               description=None, checked=None, *args, **kwargs):
        """Update a checklist item, whether edited or toggled."""
        try:
            checklist = self.get_parent_object(checklist_id)
        except Checklist.ObjectDoesNotExist:
            return DOES_NOT_EXIST

        item = checklist.edit_item(checklist_item_id, description, checked)
        return 200, {self.item_result_key: item}

    @webapi_login_required
    @webapi_response_errors(DOES_NOT_EXIST)
    @webapi_check_local_site
    def delete(self, request, api_format, checklist_id, checklist_item_id,
               *args, **kwargs):
        """Delete a checklist item in the checklist."""
        try:
            checklist = self.get_parent_object(checklist_id)
        except Checklist.ObjectDoesNotExist:
            return DOES_NOT_EXIST

        checklist.delete_item(checklist_item_id)
        return 204, {}


checklist_item_resource = ChecklistItemResource()
