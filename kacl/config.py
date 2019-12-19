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

    def is_case_sensitive(self):
        return self.__case_sensitive

    def allowed_header_titles(self):
        return self.__allowed_header_titles

    def allowed_version_sections(self):
        return self.__allowed_version_sections
