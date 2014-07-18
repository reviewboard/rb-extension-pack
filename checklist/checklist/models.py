from django.contrib.auth.models import User
from django.db import models
from djblets.util.fields import JSONField
from reviewboard.reviews.models import ReviewRequest


class ReviewChecklist(models.Model):
    """A checklist is a list of items to keep track of during a review. """

    # The user making the review.
    user = models.ForeignKey(User)

    # The review request the user is reviewing.
    review_request = models.ForeignKey(ReviewRequest)

    # Keeps track of the number of items *added* in the
    # checklist, not the current number of items in it. This
    # allows us to give unique IDs to new items.
    items_counter = models.IntegerField(default=0)

    # A JSON of all the items in the checklist. Key = ID.
    # Value = { id, finished status, description }
    checklist_items = JSONField()

    def add_item(self, item_description):
        self.items_counter += 1
        self.checklist_items[self.items_counter] = {
            'id': self.items_counter,
            'finished': False,
            'description': item_description
        }
        self.save()

    def edit_item_desc(self, itemID, item_description):
        if (str(itemID) in self.checklist_items):
            itemDict = self.checklist_items.get(str(itemID))
            itemDict['description'] = item_description
            self.save()

    def toggle_item_status(self, itemID):
        if (str(itemID) in self.checklist_items):
            itemDict = self.checklist_items.get(str(itemID))
            itemDict['finished'] = not itemDict['finished']
            self.save()

    def delete_item(self, itemID):
        if (str(itemID) in self.checklist_items):
            self.checklist_items.pop(str(itemID))
            self.save()
