# CIA extension for Review Board.
from reviewboard.extensions.base import Extension

from rbcia.client import CIAClient


class CIAExtension(Extension):
    is_configurable = True

    def __init__(self):
        Extension.__init__(self)
        self.client = CIAClient(self)
