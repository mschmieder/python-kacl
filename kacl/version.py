from .element import KACLElement
from .changes import KACLChanges
from .parser import KACLParser

import re
import semver


class KACLVersion(KACLElement):
    def __init__(self, element=KACLElement(), version="", date="", sections=None, link=None):
        KACLElement.__init__(self,
                             raw=element.raw(),
                             title=element.title(),
                             body=element.body(),
                             line_number=element.line_number())
        self.__date = date
        self.__version = version
        if sections is None:
            self.__sections = dict()
        else:
            self.__sections = sections
        self.__link_reference = None
        self.set_link(link)

    def link(self):
        if self.__link_reference:
            return self.__link_reference.body()

    def set_link(self, link):
        if isinstance(link, KACLElement):
            self.__link_reference = link
        elif link != None:
            self.__link_reference = KACLElement(title=self.version(), body=link)

    def has_link_reference(self):
        if not self.__link_reference:
            return False
        else:
            return (self.__link_reference.body() != None and len(self.__link_reference.body()))

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

    def semver(self):
        return semver.parse(self.version())

    def set_version(self, version):
        self.__version = version

    def sections(self):
        if not len(self.__sections) and len(self.body().strip()):
            self.__sections = dict()
            sections = KACLParser.parse_header(text=self.body(),
                                               start_depth=3,
                                               end_depth=3,
                                               line_offset=self.line_number())
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
        if section not in self.sections():
            self.__sections[section] = KACLChanges(KACLElement(
                title=section, body="", line_number=None))
        self.__sections[section].add(change)
