"""API resources for the checklist extension."""

from rbchecklist.resources.checklist_item import checklist_item_resource
from rbchecklist.resources.checklist_resource import checklist_resource
from rbchecklist.resources.checklist_template import \
    checklist_template_resource


__all__ = [
    'checklist_resource',
    'checklist_item_resource',
    'checklist_template_resource',
]
