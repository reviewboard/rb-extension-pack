"""Ship It! ASCII Art extension for Review Board."""

from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import SignalHook
from reviewboard.reviews.signals import review_published


art_basic = r"""
      _~
   _~)_)_~
  )_))_))_)
  _!__!__!_
  \______t/
~~~~~~~~~~~~~
"""

art_juggernaut_small = r"""
    __4___
 _  \ \ \ \
<'\ /_/_/_/
 ((____!___/)
  \\0\\0\\0\\0\/
 ~~~~~~~~~~~
"""

art_juggernaut_big = r"""
                       _____|\
                  _.--| R B |:
                 <____|.----||
                        .---''---,
                         ;..__..'    _...
                       ,'/  ;|/..--''    \
                     ,'_/.-/':            :
                _..-'''/  /  |  \    \   _|/|
               \      /-./_ \;   \    \,;'   \
               ,\    / \:  `:\    \   //    `:`.
             ,'  \  /-._;   | :    : ::    ,.   .
           ,'     ::   /`-._| |    | || ' :  `.`.)
        _,'       |;._:: |  | |    | `|   :    `'
      ,'   `.     /   |`-:_ ; |    |  |  : \
      `--.   )   /|-._:    :          |   \ \
         /  /   :_|   ;`-._;   __..--';    : :
        /  (    ;|;-./_  _/.-:'o |   /     ' |
       /  , \._/_/_./--''/_|:|___|_,'        |
      :  /   `'-'--'----'---------'          |
      | :     O ._O   O_. O ._O   O_.      ; ;
      : `.      //    //    //    //     ,' /
    ~~~`.______//____//____//____//_______,'~
              //    //~   //    //
       ~~   _//   _//   _// ~ _//     ~
     ~     / /   / /   / /   / /  ~      ~~
          ~~~   ~~~   ~~~   ~~~
"""

art = {
    'basic': art_basic,
    'juggernaut_small': art_juggernaut_small,
    'juggernaut_big': art_juggernaut_big,
}


class AsciiArt(Extension):
    """Ship It! ASCII Art extension for Review Board."""

    def __init__(self, *args, **kwargs):
        super(AsciiArt, self).__init__(*args, **kwargs)

        self.ascii_pattern = 'basic'

        SignalHook(self, review_published, self._on_review_published)

    def _on_review_published(self, review, *args, **kwargs):
        """Handler for when a review is published.

        Args:
            review (reviewboard.reviews.models.Review):
                The review which was published.

            *args (tuple):
                Positional arguments passed through the signal.

            **kwargs (dict):
                Keyword arguments passed through the signal.
        """
        # Only add the ship-it ASCII art if this review has a ship-it.
        if review.ship_it:
            rich = hasattr(review, 'rich_text') and review.rich_text

            if rich:
                review.body_top += '\n```\n'

            review.body_top += art[self.ascii_pattern]

            if rich:
                review.body_top += '```\n'

            review.save()
