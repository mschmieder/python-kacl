from .element import KACLElement
from .version import KACLVersion
from .parser import KACLParser
from .config import KACLConfig

import re

class KACLDocument:
    def __init__(self, content, headers, versions, config=KACLConfig()):
        self.__content = content
        self.__headers = headers
        self.__versions = versions

    def validate(self):
        # 1. assume only one header
        # 1.1 assume header title is in allowed list of header titles
        # 1.1.1 check case sensitivity

        # 2. assume 'unreleased' version is available
        # 2.1 check for case sensitivity

        # 3. assume versions in valid format
        # 3.1 assume versions in descending order
        # 3.2 assume versions have date
        # 3.3 check that only allowed sections are in the version
        # 3.4 check that only list elements are in the sections

        pass

    def add(self, section, content):
        pass

    def release(self, version):
        pass

    def get(self, version):
        res = [ x for x in self.__versions if x.version() and version in x.version() ]
        if res and len(res):
            return res[0]
        return None

    def header(self):
        return self.__headers[0]

    def title(self):
        if self.__headers[0]:
            return self.__headers[0].title()
        return None

    def versions(self):
        return self.__versions

    @staticmethod
    def parse(text):
        # First check if there are link references and split the document where they begin
        link_reference_begin, link_references = KACLParser.parse_link_references(text)

        changelog_body = text
        if link_reference_begin:
            changelog_body = text[:link_reference_begin]

        # read header
        headers = KACLParser.parse_header(changelog_body, 1, 2)

        # read versions
        versions = KACLParser.parse_header(changelog_body, 2, 2)
        versions = [ KACLVersion(element=x) for x in versions ]

        # set link references into versions if available
        for v in versions:
            v.set_link(link_references.get(v.version(), None))

        return KACLDocument(content=text, headers=headers, versions=versions)
