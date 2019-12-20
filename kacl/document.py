import datetime
import re
import semver

from .element import KACLElement
from .version import KACLVersion
from .parser import KACLParser
from .config import KACLConfig
from.validation import KACLValidation

class KACLDocument:
    def __init__(self, data="", headers=[], versions=[], link_references=None, config=KACLConfig()):
        self.__data = data
        self.__headers = headers
        self.__versions = versions
        self.__link_references = link_references
        if not self.__link_references:
            self.__link_references = dict()
        self.__config = config

    def validate(self):
        """[summary]

        Returns:
            [type] -- [description]
        """
        validation = KACLValidation()
        # 1. assume only one header and starts on first line
        if len(self.__headers) == 0:
            validation.add_error(
                line=None,
                line_number=None,
                error_message="No 'Changelog' header found.")

            # we can stop here already
            return validation
        else:
            if self.header().raw() != self.header().raw().lstrip():
                validation.add_error(
                    line=None,
                    line_number=None,
                    error_message="Changelog header not placed on first line.")

        if len(self.__headers) > 1:
            for header in self.__headers[1:]:
                validation.add_error(
                    line=header.raw(),
                    line_number=header.line_number(),
                    error_message="Unexpected additional top-level heading found.",
                    start_character_pos=0,
                    end_character_pos=len(header.raw())
                )

        # 1.1 assume header title is in allowed list of header titles
        if self.header().title() not in self.__config.allowed_header_titles():
            header = self.header()
            start_pos = header.raw().find(header.title())
            end_pos = start_pos+len(header.title())
            validation.add_error(
                line=header.raw(),
                line_number=header.line_number(),
                error_message=f"Header title not valid. Options are [{','.join(self.__config.allowed_header_titles())}]",
                start_character_pos=start_pos,
                end_character_pos=end_pos
            )

        # 2. assume 'unreleased' version is available
        if self.get('Unreleased') == None:
            validation.add_error(
                line=None,
                line_number=None,
                error_message="'Unreleased' section is missing from the Changelog"
            )

        # 3. assume versions in valid format
        versions = self.versions()
        for v in versions:
            if "Unreleased" != v.version():
                raw = v.raw()
                regex = KACLParser.semver_regex
                regex_error = f'#\s+(.*)\s+'
                if v.link():
                    regex = f'#\s+\[{KACLParser.semver_regex}\]'
                    regex_error = r'#\s+\[(.*)\]'
                if not KACLParser.parse_sem_ver(raw, regex):
                    start_pos
                    end_pos
                    m = re.match(regex_error, raw)
                    if m:
                        start_pos = raw.find(m.group(1))
                        end_pos = start_pos+len(m.group(1))
                    validation.add_error(
                        line=raw,
                        line_number=v.line_number(),
                        error_message=f"Version is not a valid semantic version.",
                        start_character_pos=start_pos,
                        end_character_pos=end_pos
                    )

        # 3.1 assume versions in descending order
        for i in range(len(versions)-1):
            try:
                v0 = versions[i]
                v1 = versions[i+1]
                if semver.compare(v0.version(), v1.version()) < 1:
                    validation.add_error(
                        line=v1.raw(),
                        line_number=v1.line_number(),
                        error_message="Versions are not in descending order.",
                        start_character_pos=0,
                        end_character_pos=len(v1.raw())
                    )
            except:
                pass

        # 3.2 assume versions have a valid date
        for v in versions:
            if "Unreleased" != v.version():
                if not v.date() or len(v.date()) < 1:
                    validation.add_error(
                        line=v.raw(),
                        line_number=v.line_number(),
                        error_message="Versions need to be decorated with a release date 'YYYY-MM-DD'",
                        start_character_pos=0,
                        end_character_pos=len(v.raw())
                    )
                if v.date() and not re.match(r'\d\d\d\d-[0-1][0-9]-[0-3][0-9]', v.date()):
                    start_pos = v.raw().find(v.date())
                    end_pos = start_pos+len(v.date())
                    validation.add_error(
                        line=v.raw(),
                        line_number=v.line_number(),
                        error_message="Date does not match format 'YYYY-MM-DD'",
                        start_character_pos=start_pos,
                        end_character_pos=end_pos
                    )

        # 3.3 check that only allowed sections are in the version
            sections = v.sections()
            for title, element in sections.items():
                if title not in self.__config.allowed_version_sections():
                    start_pos = element.raw().find(title)
                    end_pos = start_pos+len(title)
                    validation.add_error(
                        line=element.raw(),
                        line_number=element.line_number(),
                        error_message=f'"{title}" is not a valid section for a version. Options are [{",".join( self.__config.allowed_version_sections())}]',
                        start_character_pos=start_pos,
                        end_character_pos=end_pos
                    )
        # 3.4 check that only list elements are in the sections
                # 3.4.1 bring everything into a single line
                body = element.body()
                body_clean = re.sub(r'\n\s+', '', body)
                lines = body_clean.split('\n')
                non_list_lines = [x for x in lines if not x.strip(
                ).startswith('-') and len(x.strip()) > 0]
                if len(non_list_lines) > 0:
                    validation.add_error(
                        line=body.strip(),
                        line_number=element.line_number(),
                        error_message='Section does contain more than only listings.'
                    )

        # 4 link references
        # 4.1 check that there are only linked references
        version_strings = [v.version() for v in versions]
        for v, link in self.__link_references.items():
            if v not in version_strings:
                validation.add_error(
                    line=link.raw(),
                    line_number=link.line_number(),
                    error_message=f"Link not referenced anywhere in the document",
                    start_character_pos=0,
                    end_character_pos=len(link.raw())
                )

        return validation

    def is_valid(self):
        """[summary]
        Returns:
            [type] -- [description]
        """
        validation_results = self.validate()
        return validation_results.is_valid()

    def add(self, section, data):
        """[summary]

        Arguments:
            section {[type]} -- [description]
            data {[type]} -- [description]
        """
        unreleased_version = self.get('Unreleased')
        unreleased_version.add(section, data)

    def release(self, version, link=None):
        """[summary]

        Arguments:
            version {[type]} -- [description]

        Keyword Arguments:
            link {[type]} -- [description] (default: {None})
        """
        # get current unreleased changes
        unreleased_version = self.get('Unreleased')

        # remove current unrelease version from list
        self.__versions.pop(0)

        # convert unreleased version to version
        self.__versions.insert(0, KACLVersion(version=version,
                                              link=KACLElement(
                                                  title=version, body=link),
                                              date=datetime.datetime.now().strftime("%Y-%m-%d"),
                                              sections=unreleased_version.sections()))
        # add new unreleased section
        self.__versions.insert(0, KACLVersion(version='Unreleased'))

    def get(self, version):
        """[summary]

        Arguments:
            version {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        res = [x for x in self.__versions if x.version()
               and version in x.version()]
        if res and len(res):
            return res[0]

    def header(self):
        """[summary]

        Returns:
            [type] -- [description]
        """
        return self.__headers[0]

    def title(self):
        """[summary]

        Returns:
            [type] -- [description]
        """
        if self.__headers[0]:
            return self.__headers[0].title()
        return None

    def versions(self):
        """[summary]

        Returns:
            [type] -- [description]
        """
        return self.__versions

    @staticmethod
    def parse(data):
        """[summary]

        Arguments:
            data {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        # First check if there are link references and split the document where they begin
        link_reference_begin, link_references = KACLParser.parse_link_references(
            data)

        changelog_body = data
        if link_reference_begin:
            changelog_body = data[:link_reference_begin]

        # read header
        headers = KACLParser.parse_header(changelog_body, 1, 2)

        # read versions
        versions = KACLParser.parse_header(changelog_body, 2, 2)
        versions = [KACLVersion(element=x) for x in versions]

        # set link references into versions if available
        for v in versions:
            v.set_link(link_references.get(v.version(), None))

        return KACLDocument(data=data, headers=headers, versions=versions, link_references=link_references)
