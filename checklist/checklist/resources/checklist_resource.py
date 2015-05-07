from django.contrib.auth.models import User
from djblets.webapi.decorators import webapi_request_fields
from reviewboard.webapi.base import WebAPIResource
from reviewboard.webapi.decorators import (webapi_check_local_site,
                                           webapi_login_required)
from reviewboard.webapi.resources import resources

from checklist.models import ReviewChecklist


class ChecklistResource(WebAPIResource):
    name = 'checklist'
    model = ReviewChecklist
    uri_object_key = 'checklist_id'
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')

    fields = {
        'id': {
            'type': int,
            'description': 'The numeric ID of the checklist review.'
        },
        'items_counter': {
            'type': int,
            'description': 'Number of items added in the checklist.'
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

    @webapi_request_fields(
        required={
            'user_id': {
                'type': int,
                'description': 'The id of the user creating the checklist.'
            },
            'review_request_id': {
                'type': int,
                'description': 'The id of the review request.'
            }
        }
    )
    @webapi_login_required
    @webapi_check_local_site
    def create(self, request, user_id=None, *args, **kwargs):
        """Creates a new checklist."""

        user = User.objects.get(pk=user_id)
        review_request = resources.review_request.get_object(request,
                                                             args, **kwargs)

        new_checklist, created = ReviewChecklist.objects.get_or_create(
            user=user,
            review_request=review_request)

        status_code = 201 if created else 200
        return status_code, {self.item_result_key: new_checklist}

    @webapi_login_required
    @webapi_request_fields(
        optional={
            'user_id': {
                'type': int,
                'description': 'The id of the user creating the checklist.'
            },
            'review_request_id': {
                'type': int,
                'description': 'The id of the review request.'
            },
            'checklist_item_id': {
                'type': int,
                'description': 'The id of the checklist item to edit or '
                               'delete.'
            },
            'item_description': {
                'type': str,
                'description': 'The description of the checklist item.'
            },
            'toggle': {
                'type': str,
                'description': 'If present, status of the item should '
                               'be toggled.'
            }
        }
    )
    @webapi_check_local_site
    def update(self, request, checklist_item_id=None, user_id=None,
               item_description=None, toggle=None, *args, **kwargs):
        """Add, edit, delete or update the status of an item on the list"""

        user = User.objects.get(pk=user_id)
        review_request = resources.review_request.get_object(request, args,
                                                             **kwargs)
        checklist = ReviewChecklist.objects.filter(
            user=user, review_request=review_request).first()

        if checklist_item_id is None and item_description is not None:
            # If there is no checklist_item_id, we are adding a new item
            checklist.add_item(item_description)
        elif checklist_item_id is not None and item_description is not None:
            checklist.edit_item_desc(checklist_item_id, item_description)
        elif (checklist_item_id is not None and item_description is None
              and toggle is None):
            checklist.delete_item(checklist_item_id)
        elif checklist_item_id is not None and toggle is not None:
            # If toggle is present, we toggle the status of the checklist item
            checklist.toggle_item_status(checklist_item_id)

        return 200, {self.item_result_key: checklist}


checklist_resource = ChecklistResource()
