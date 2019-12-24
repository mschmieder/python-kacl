import os

class KACLConfig:
    def __init__(self, config_file=None):
        self.__allowed_header_titles = ['Changelog', 'Change Log']

        self.__allowed_version_sections = ["Added",
                                           "Changed",
                                           "Deprecated",
                                           "Removed",
                                           "Fixed",
                                           "Security"]
        self.__case_sensitive = True

        self.__default_content = [
            "All notable changes to this project will be documented in this file.",
            "The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)."
        ]

        self.__changelog_file = os.path.join(os.getcwd(), 'CHANGELOG.md')

        self.__git_create_commit = False
        self.__git_commit_message = "Updated version: {latest_version} -> {new_version}"
        self.__git_commit_additional_files = []

        self.__git_create_tag = False
        self.__git_tag_name = "v{new_version}"
        self.__git_tag_description = "Released version: {new_version}"

    def is_case_sensitive(self):
        return self.__case_sensitive

    def allowed_header_titles(self):
        return self.__allowed_header_titles

    def allowed_version_sections(self):
        return self.__allowed_version_sections

    def default_content(self):
        return self.__default_content

    def git_tag_name(self):
        return self.__git_tag_name

    def git_tag_description(self):
        return self.__git_tag_description

    def changelog_file(self):
        return self.__changelog_file

    def set_changelog_file(self, file_path):
        self.__changelog_file = file_path

    def git_create_tag(self):
        return self.__git_create_tag

    def git_create_commit(self):
        return self.__git_create_commit

    def git_commit_message(self):
        return self.__git_commit_message

    def git_commit_additional_files(self):
        return self.__git_commit_additional_files