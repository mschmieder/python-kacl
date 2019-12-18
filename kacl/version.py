from .element import KACLElement
from .changes import KACLChanges
from .parser import KACLParser

import re

semver_regex = r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?'

class KACLVersion(KACLElement):
    def __init__(self, element):
        KACLElement.__init__(self, title=element.title(), body=element.body(), start=element.start(), end=element.end())
        self.__date = None
        self.__version = None
        self.__changes = None

    def date(self):
        if self.__date:
            return self.__date
        else:
            title = self.title()
            m = re.search(r'\d\d\d\d-\d\d-\d\d', title)
            if m:
                self.__date = m.group().strip()

        return self.__date

    def version(self):
        if self.__version:
            return self.__version
        else:
            title = self.title()
            m = re.search(semver_regex, title)
            if m:
                self.__version = m.group().strip()

        return self.__version

    def sections(self):
        if self.__changes:
            return self.__changes
        else:
            self.__changes = dict()
            sections = KACLParser.parse_header(self.body(), 3)
            for section in sections:
                sec = KACLChanges(section)
                self.__changes[sec.title()] = sec
        return self.__changes

    def changes(self, section):
        sections = self.sections()
        if sections and section in sections:
            return sections[section]

        return None