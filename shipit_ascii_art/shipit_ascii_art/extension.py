# shipit_ascii_art Extension for Review Board.
from reviewboard.extensions.base import Extension

from shipit_ascii_art.handlers import SignalHandlers


class AsciiArt(Extension):
    is_configurable = True

    def __init__(self, *args, **kwargs):
        super(AsciiArt, self).__init__(*args, **kwargs)
        self.signal_handlers = SignalHandlers(self)
        # This variable will be changed or refactored when
        # Ascii art is made configurable
        self.ascii_pattern = "basic"
