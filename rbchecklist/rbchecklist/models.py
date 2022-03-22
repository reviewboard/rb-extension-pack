"""Models for the checklist extension."""

from django.contrib.auth.models import User
from django.db import models
from djblets.db.fields import JSONField
from reviewboard.reviews.models import ReviewRequest


class ReviewChecklist(models.Model):
    """A checklist is a list of items to keep track of during a review.

    Items are stored in JSON format in the following manner:

    ::

      checklist_items: {
          id: {
              'id': '123',
              'checked': true,
              'description': 'Remember to look for bugs'
          },
          ...
      }
    """

    # The user making the review.
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # The review request the user is reviewing.
    review_request = models.ForeignKey(ReviewRequest, on_delete=models.CASCADE)

    # Used to provide unique ids for each checklist item.
    next_item_id = models.IntegerField(default=0)

    # A JSON blob of all the items in the checklist.
    checklist_items = JSONField()

    def add_item(self, item_description):
        """Add and return the new checklist item.

        Args:
            item_description (str):
                The text for the checklist item.

        Returns:
            dict:
            The newly-added checklist item.
        """
        item = {
            'id': self.next_item_id,
            'checked': False,
            'description': item_description
        }
        self.checklist_items['%d' % self.next_item_id] = item
        self.next_item_id += 1

        self.save()
        return item

    def edit_item(self, item_id, item_description=None, checked=None):
        """Modify and return the checklist item specified.

        Args:
            item_id (int):
                The ID of the item to modify.

            item_description (str, optional):
                The new text to set on the item.

            checked (bool, optional):
                Whether the item should be checked.

        Returns:
            dict:
            The edited checklist item.
        """
        if isinstance(item_id, int):
            item_id = '%d' % item_id

        if item_id in self.checklist_items:
            item = self.checklist_items.get(item_id)

            if item_description is not None:
                item['description'] = item_description

            if checked is not None:
                item['checked'] = checked

            self.save()
            return item

    def delete_item(self, item_id):
        """Delete the checklist item.

        Args:
            item_id (int):
                The ID of the item to delete.
        """
        if isinstance(item_id, int):
            item_id = '%d' % item_id

        if item_id in self.checklist_items:
            self.checklist_items.pop(item_id)
            self.save()

    class Meta:
        """Metadata for the Checklist model."""

        app_label = 'rbchecklist'


class ChecklistTemplate(models.Model):
    """A checklist template defines a collection of checklist items.

    Each template can be imported into a checklist. Items are stored in JSON
    format as a single array of checklist items.
    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    items = JSONField()

    class Meta:
        """Metadata for the ChecklistTemplate model."""

        app_label = 'rbchecklist'
