import datetime
import re
import semver
import os
import git

from .element import KACLElement
from .version import KACLVersion
from .parser import KACLParser
from .config import KACLConfig
from .link_provider import LinkProvider
from.validation import KACLValidation

WINDOWS_LINE_ENDING = r'\r\n'
UNIX_LINE_ENDING = r'\n'

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
        """Validates the current changelog and returns KACLValidation object containing all information

        Returns:
            [KACLValidation] -- object holding all error information
        """
        validation = KACLValidation()
        # 1. assert only one header and starts on first line
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

        # 1.1 assert header title is in allowed list of header titles
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

        # 1.2 assert default content is in the header section
        for default_line in self.__config.default_content():
            if default_line not in self.header().body():
                header = self.header()
                start_pos = header.raw().find(header.title())
                end_pos = start_pos+len(header.title())
                validation.add_error(
                    line=header.raw(),
                    line_number=header.line_number(),
                    error_message=f"Missing default content '{default_line}'",
                    start_character_pos=start_pos,
                    end_character_pos=end_pos
                )

        # 2. assert 'unreleased' version is available
        # if self.get('Unreleased') == None:
        #     validation.add_error(
        #         line=None,
        #         line_number=None,
        #         error_message="'Unreleased' section is missing from the Changelog"
        #     )

        # 3. assert versions in valid format
        versions = self.versions()
        for v in versions:
            if "Unreleased" != v.version():
                raw = v.raw()
                regex = KACLParser.semver_regex
                regex_error = r'#\s+(.*)\s+'
                if v.link():
                    regex = f'#\\s+\\[{KACLParser.semver_regex}\\]'
                    regex_error = r'#\s+\[(.*)\]'
                if not KACLParser.parse_sem_ver(raw, regex):
                    start_pos = 0
                    end_pos = 0
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

        # 3.1 assert versions in descending order
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

        # 3.2 assert versions have a valid date
        for v in versions:
            if "Unreleased" != v.version():
                if not v.date() or len(v.date()) < 1:
                    validation.add_error(
                        line=v.raw(),
                        line_number=v.line_number(),
                        error_message="Versions need to be decorated with a release date in the following format 'YYYY-MM-DD'",
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
        # 3.5 make sure that every version that has content has it's content in a section
            if len(v.sections()) == 0 and len(v.body().strip()) != 0:
                validation.add_error(
                    line=v.raw(),
                    line_number=v.line_number(),
                    error_message=f'Version "{v.version()}" has change elements outside of a change section.'
                )

        # 3.6 Check that a link exists for linked versions
            if '[' in v.raw() and ']' in v.raw() and not v.has_link_reference():
                validation.add_error(
                    line=v.raw(),
                    line_number=v.line_number(),
                    error_message=f'Version "{v.version()}" is linked, but no link reference found in changelog file.',
                    start_character_pos=v.raw().find('['),
                    end_character_pos=v.raw().find(']')
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
        """Checks if the current changelog is valid
        Returns:
            [bool] -- true if valid false if not
        """
        validation_results = self.validate()
        return validation_results.is_valid()

    def has_changes(self):
        unreleased_version = self.get('Unreleased')
        if not unreleased_version:
            return False

        sections = unreleased_version.sections()
        if not sections or len(sections) == 0:
            return False

        for pair in sections.items():
            if pair[1] and len(pair[1].items()) > 0:
                return True

        return False

    def add(self, section, data):
        """adds a new change to a given section in the 'unreleased' version

        Arguments:
            section {[str]} -- section to add data to
            data {[str]} -- change information
        """
        unreleased_version = self.get('Unreleased')
        if unreleased_version == None:
            unreleased_version = KACLVersion(version="Unreleased")
            self.__versions.insert(0, unreleased_version)
        unreleased_version.add(section.capitalize(), data)

    def release(self, version=None, link=None, auto_link=False, increment=None):
        """Creates a new release version by copying the 'unreleased' changes into the
        new version

        Keyword Arguments:
            link {[str]} -- url the version will be linked with (default: {None})
            version {[str]} -- semantic versioning string
            increment {[str]} -- use either 'patch', 'minor', or 'major' to automatically increment the last version
        """
        if increment:
            v = self.current_version()
            if v:
                sv = semver.VersionInfo.parse(v)
                if 'patch' == increment:
                    sv = sv.bump_patch()
                elif 'minor' == increment:
                    sv = sv.bump_minor()
                elif 'major' == increment:
                    sv = sv.bump_major()
                version = str(sv)
            else:
                raise Exception("No previously released version found. Incrementing not possible")

        # check that version is a valid semantic version
        semver.parse(version) # --> will throw a ValueError if version is not a valid semver

        # check if there are changes to release
        if self.has_changes() is False:
            raise Exception("The current changlog has no changes. You can only release if changes are available.")

        # check if the version already exists
        if self.get(version) != None:
            raise Exception(f"The version '{version}' already exists in the changelog. You cannot release the same version twice.")

        # check if new version is greater than the last one
        #   1. there has to be an 'unreleased' section
        #   2. All other versions are in descending order
        version_list = self.versions()
        if len(version_list) > 1: # versions[0] --> unreleased
            last_version = version_list[1].version()
            if semver.compare(version, last_version) < 1:
                raise Exception(f"The version '{version}' cannot be released since it is smaller than the preceeding version '{last_version}'.")

        # get current unreleased changes
        unreleased_version = self.get('Unreleased')

        # remove current unrelease version from list
        self.__versions.pop(0)

        self.__versions.insert(0, KACLVersion(version="Unreleased", link=unreleased_version.link()))

        # convert unreleased version to version
        self.__versions.insert(1, KACLVersion(version=version,
                                              link=KACLElement(
                                                  title=version, body=link),
                                              date=datetime.datetime.now().strftime("%Y-%m-%d"),
                                              sections=unreleased_version.sections()))

        if auto_link:
            link_provider = self.__get_link_provider()
            for i in range(2):
                fargs = {
                    "version": self.__versions[i].version(),
                    "previous_version": self.__versions[i+1].version(),
                    "latest_version": version
                }
                if 'unreleased' in self.__versions[i].version().lower():
                    self.__versions[i].set_link( link_provider.unreleased_changes(**fargs) )
                else:
                    self.__versions[i].set_link( link_provider.compare_versions(**fargs) )

    def get(self, version):
        """Returns the selected version

        Arguments:
            version {[str]} -- semantic versioning string

        Returns:
            [KACLVersion] -- version object with all information
        """
        res = [x for x in self.__versions if x.version()
               and version.capitalize() == x.version()]
        if res and len(res):
            return res[0]

    def current_version(self):
        """returns the current version (last released)

        Returns:
            [str] -- latest released version, None if none is available
        """
        version_list = self.versions()
        for v in version_list:
            if v.version().lower() != 'unreleased':
                return v.version()

    def generate_links(self, host_url=None, compare_versions_template=None, unreleased_changes_template=None, initial_version_template=None):
        """automatically generates links for all versions

        Returns: None
        """
        link_provider = self.__get_link_provider(host_url=host_url,
                                                 compare_versions_template=compare_versions_template,
                                                 unreleased_changes_template=unreleased_changes_template,
                                                 initial_version_template=initial_version_template)

        versions = self.versions()
        if len(versions) > 1:
            for i in range(len(versions)-1):
                fargs = {
                    "version": versions[i].version(),
                    "previous_version": versions[i+1].version(),
                    "latest_version": self.current_version()
                }

                if 'unreleased' in versions[i].version().lower():
                    versions[i].set_link( link_provider.unreleased_changes(**fargs) )
                else:
                    versions[i].set_link( link_provider.compare_versions(**fargs) )
            versions[-1].set_link( link_provider.initial_version(**fargs) )
        elif len(versions) == 1:
            fargs = {
                "version": versions[0].version(),
                "latest_version": self.current_version()
            }

            if 'unreleased' in versions[0].version().lower():
                versions[0].set_link( link_provider.initial_version(version="master") )
            else:
                versions[0].set_link( link_provider.initial_version(**fargs) )


    def header(self):
        """Gives access to the top level heading element

        Returns:
            [KACLElement] -- object holding all information of the top level heading
        """
        if self.__headers and len(self.__headers) > 0:
            return self.__headers[0]

    def title(self):
        """Returns the title of the changelog

        Returns:
            [str] -- title of the changelog
        """
        if self.__headers and len(self.__headers) > 0:
            return self.__headers[0].title()
        return None

    def versions(self):
        """Returns a list of all available versions

        Returns:
            [list] -- list of KACLVersions
        """
        return self.__versions

    def set_config(self, config):
        self.__config = config

    def config(self):
        return self.__config

    @staticmethod
    def init():
        return KACLDocument.parse("""# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased
        """)

    @staticmethod
    def parse(data):
        """Parses a given text object and returns the KACLDocument

        Arguments:
            data {[str]} -- markdown text holding the changelog

        Returns:
            [KACLDocument] -- object holding all information
        """

        data_lf = data.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)

        # First check if there are link references and split the document where they begin
        link_reference_begin, link_references = KACLParser.parse_link_references(data_lf)

        changelog_body = data_lf
        if link_reference_begin:
            changelog_body = data_lf[:link_reference_begin]

        # read header
        headers = KACLParser.parse_header(changelog_body, 1, 2)

        # read versions
        versions = KACLParser.parse_header(changelog_body, 2, 2)
        versions = [KACLVersion(element=x) for x in versions]

        # set link references into versions if available
        for v in versions:
            v.set_link(link_references.get(v.version(), None))

        return KACLDocument(data=data, headers=headers, versions=versions, link_references=link_references)


    def __get_link_provider(self, host_url=None, compare_versions_template=None, unreleased_changes_template=None, initial_version_template=None):
        host_url = host_url if host_url else self.__config.link_host_url()
        compare_versions_template = compare_versions_template if compare_versions_template else self.__config.links_compare_versions_template()
        unreleased_changes_template = unreleased_changes_template if unreleased_changes_template else self.__config.links_unreleased_changes_template()
        initial_version_template = initial_version_template if initial_version_template else self.__config.links_initial_version_template()

        if host_url is None:
            repo = git.Repo(os.getcwd())
            remote = repo.remote()
            for url in remote.urls:
                host_url = url
                break

        return LinkProvider(host_url=host_url,
                            compare_versions_template=compare_versions_template,
                            unreleased_changes_template=unreleased_changes_template,
                            initial_version_template=initial_version_template)
