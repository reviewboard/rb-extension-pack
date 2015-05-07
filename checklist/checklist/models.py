from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils import six
from djblets.db.fields import JSONField
from reviewboard.reviews.models import ReviewRequest


class ReviewChecklist(models.Model):
    """A checklist is a list of items to keep track of during a review.

    Items are stored in JSON format in the following manner:

    ::

      checklist_items: {
          id: {
              'id': six.text_type,
              'checked': bool,
              'description': six.text_type
          },
          ...
      }
    """

    # The user making the review.
    user = models.ForeignKey(User)

    # The review request the user is reviewing.
    review_request = models.ForeignKey(ReviewRequest)

    # Used to provide unique ids for each checklist item.
    next_item_id = models.IntegerField(default=0)

    # A JSON blob of all the items in the checklist.
    checklist_items = JSONField()

    def add_item(self, item_description):
        """Add and return the new checklist item."""
        item = {
            'id': self.next_item_id,
            'checked': False,
            'description': item_description
        }
        self.checklist_items[self.next_item_id] = item
        self.next_item_id += 1

        self.save()
        return item

    def edit_item(self, item_id, item_description, checked):
        """Modify and return the checklist item specified."""
        if six.text_type(item_id) in self.checklist_items:
            item = self.checklist_items.get(six.text_type(item_id))

            if item_description is not None:
                item['description'] = item_description

            if checked is not None:
                item['checked'] = checked

            self.save()
            return item

    def delete_item(self, item_id):
        """Delete the checklist item."""
        if six.text_type(item_id) in self.checklist_items:
            self.checklist_items.pop(six.text_type(item_id))
            self.save()


class ChecklistTemplate(models.Model):
    """A checklist template defines a collection of checklist items.

    Each template can be imported into a checklist. Items are stored in JSON
    format as a single array of checklist items.
    """

    owner = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    items = JSONField()
