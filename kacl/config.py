import os
import yaml
from box import Box

class KACLConfig:
    def __init__(self, config_file=None):
        default_config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', 'kacl-default.yml')
        with open(default_config_file, 'r') as df:
            self.__config = yaml.safe_load(df)
        if config_file:
            with open(os.path.expanduser(config_file), 'r') as f:
                KACLConfig.merge(self.__config, yaml.safe_load(f))

        self.__config = Box(self.__config)

    def allowed_header_titles(self):
        return self.__config.kacl.allowed_header_titles

    def allowed_version_sections(self):
        return self.__config.kacl.allowed_version_sections

    def default_content(self):
        return self.__config.kacl.default_content

    def git_tag_name(self):
        return self.__config.kacl.git.tag_name

    def git_tag_description(self):
        return self.__config.kacl.git.tag_description

    def changelog_file_path(self):
        return self.__config.kacl.file

    def set_changelog_file_path(self, file_path):
        self.__config.kacl.file = file_path

    def git_create_tag(self):
        return self.__config.kacl.git.tag

    def git_create_commit(self):
        return self.__config.kacl.git.commit

    def git_commit_message(self):
        return self.__config.kacl.git.commit_message

    def git_commit_additional_files(self):
        return self.__config.kacl.git.commit_additional_files

    @staticmethod
    def merge(a, b, path=None):
        """ merge two dictionaries
        :param a: dictionary the values will be merged into
        :param b: dictionary the values will be used when overwriting values
        :param path:
        :return:
        """
        if path is None:
            path = []
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    KACLConfig.merge(a[key], b[key], path + [str(key)])
                elif a[key] == b[key]:
                    pass  # same leaf value
                else:
                    a[key] = b[key]

            else:
                a[key] = b[key]
        return a