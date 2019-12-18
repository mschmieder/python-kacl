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

    def dump(self, file=None):
        pass

    def title(self):
        if self.__headers:
            return self.__headers[0].title()
        return None

    def versions(self):
        return self.__versions

    @staticmethod
    def parse(text):
        headers = KACLParser.parse_header(text, 1)
        versions = KACLParser.parse_header(text, 2)
        versions = [ KACLVersion(x) for x in versions ]

        return KACLDocument(content=text, headers=headers, versions=versions)
