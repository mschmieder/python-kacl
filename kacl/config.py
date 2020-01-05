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
                self.__config.update(yaml.safe_load(f))

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