from reviewboard.reviews.signals import review_published

from shipit_ascii_art.asciiart import ship_art_dict


class SignalHandlers(object):
    """
    Signal handlers for reviewboard signals.
    """

    def __init__(self, extension):
        """Initialize and connect all the signals"""
        self.extension = extension

        # Connect the handlers.
        review_published.connect(self._review_published,
                                 dispatch_uid='shipit_ascii_art_extension')

    def disconnect(self):
        """Disconnect the signal handlers"""
        review_published.disconnect(self._review_published)

    def _review_published(self, **kwargs):
        review = kwargs.get('review')

        # Only add the ship-it ascii art if this review has a ship-it
        if review.ship_it:
            rich = hasattr(review, 'rich_text') and review.rich_text

            if rich:
                review.body_top += '\n```\n'

            review.body_top += ship_art_dict[self.extension.ascii_pattern]

            if rich:
                review.body_top += '```\n'

            review.save()
