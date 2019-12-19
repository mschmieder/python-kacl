from .element import KACLElement
from .changes import KACLChanges
from .parser import KACLParser

import re

class KACLVersion(KACLElement):
    def __init__(self, element, link=None):
        KACLElement.__init__(self, title=element.title(), body=element.body(), start=element.start(), end=element.end())
        self.__date = None
        self.__version = None
        self.__changes = None
        self.__link = link

    def link(self):
        return self.__link

    def set_link(self, link):
        self.__link = link

    def has_link_reference(self):
        return (self.__link != None)

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
            version = KACLParser.parse_sem_ver(title)
            if version:
                self.__version = version
            elif 'unreleased' in title.lower():
                self.__version = "Unreleased"

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