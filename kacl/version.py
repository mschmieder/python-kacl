from .element import KACLElement
from .changes import KACLChanges
from .parser import KACLParser

import re


class KACLVersion(KACLElement):
    def __init__(self, element=KACLElement(), version="", date="", sections=None, link=None):
        KACLElement.__init__(self, title=element.title(
        ), body=element.body(), start=element.start(), end=element.end())
        self.__date = date
        self.__version = version
        if sections is None:
            self.__sections = dict()
        else:
            self.__sections = sections
        self.__link = link

    def link(self):
        return self.__link

    def set_link(self, link):
        self.__link = link

    def has_link_reference(self):
        return (self.__link != None)

    def date(self):
        if not len(self.__date):
            title = self.title()
            m = re.search(r'\d\d\d\d-\d\d-\d\d', title)
            if m:
                self.__date = m.group().strip()

        return self.__date

    def version(self):
        if not len(self.__version):
            title = self.title()
            version = KACLParser.parse_sem_ver(title)
            if version:
                self.__version = version
            elif 'unreleased' in title.lower():
                self.__version = "Unreleased"

        return self.__version

    def set_version(self, version):
        self.__version = version

    def sections(self):
        if not len(self.__sections) and len(self.body().strip()):
            self.__sections = dict()
            sections = KACLParser.parse_header(self.body(), 3)
            for section in sections:
                sec = KACLChanges(section)
                self.__sections[sec.title()] = sec
        return self.__sections

    def changes(self, section):
        sections = self.sections()
        if sections and section in sections:
            return sections[section]

        return None

    def add(self, section, change):
        if section not in self.__sections:
            self.__sections[section] = KACLChanges(KACLElement(
                title=section, body="", start=None, end=None))
        self.__sections[section].add(change)
