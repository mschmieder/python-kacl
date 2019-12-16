from .document import KACLDocument

import re

class Parser:
    def __init__(self, stream):
        self.stream = stream
        self.allowed_header = [
            'Changelog',
            'Change Log',
        ]

    def dispose(self):
        self.stream = None

    def parse(self):
        document = self.stream.read()

        return KACLDocument()