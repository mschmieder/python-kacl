class KACLConfig:
    def __init__(self):
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

    def is_case_sensitive(self):
        return self.__case_sensitive

    def allowed_header_titles(self):
        return self.__allowed_header_titles

    def allowed_version_sections(self):
        return self.__allowed_version_sections

    def default_content():
        return self.__default_content