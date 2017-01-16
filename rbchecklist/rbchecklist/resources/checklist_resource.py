from __future__ import unicode_literals

from djblets.webapi.decorators import (webapi_login_required,
                                       webapi_request_fields)
from reviewboard.webapi.base import WebAPIResource
from reviewboard.webapi.decorators import webapi_check_local_site
from reviewboard.webapi.resources import resources

from rbchecklist.models import ReviewChecklist
from rbchecklist.resources import checklist_item_resource


class ChecklistResource(WebAPIResource):
    name = 'checklist'
    model = ReviewChecklist
    uri_object_key = 'checklist_id'
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    item_child_resources = [checklist_item_resource]  # Just for url patterns.

    fields = {
        'id': {
            'type': int,
            'description': 'The numeric ID of the checklist review.'
        },
        'checklist_items': {
            'type': str,
            'description': 'Items in checklist.'
        }
    }

    def has_access_permissions(self, request, checklist, *args, **kwags):
        return checklist.user == request.user

    def has_delete_permissions(self, request, checklist, *args, **kwags):
        return checklist.user == request.user

    def get_queryset(self, request, is_list=False, *args, **kwargs):
        """Return only checklists that belong to the user."""

        return self.model.objects.filter(user=request.user)

    @webapi_request_fields(
        required={
            'review_request_id': {
                'type': int,
                'description': 'The id of the review request.'
            }
        }
    )
    @webapi_login_required
    @webapi_check_local_site
    def create(self, request, *args, **kwargs):
        """Get or create a new checklist."""
        review_request = resources.review_request.get_object(request,
                                                             args, **kwargs)

        new_checklist, created = ReviewChecklist.objects.get_or_create(
            user=request.user,
            review_request=review_request)

        status_code = 201 if created else 200
        return status_code, {self.item_result_key: new_checklist}


checklist_resource = ChecklistResource()
