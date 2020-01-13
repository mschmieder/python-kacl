import re

class LinkProvider:
    def __init__(self, host_url=None, compare_versions_template=None, unreleased_changes_template=None, initial_version_template=None):
        self.host_url = self.__sanatize_url(host_url)
        self.compare_versions_template = compare_versions_template
        self.unreleased_changes_template = unreleased_changes_template
        self.initial_version_template = initial_version_template

    def __sanatize_url(self, url):
        if url:
            regExpr = r'git@(.*):(.*).git'
            m = re.search(regExpr, url)
            if m:
                return f'https://{m.group(1)}/{m.group(2)}'
        return url

    def compare_versions(self, version=None, previous_version=None, latest_version=None):
        return self.compare_versions_template.format(
            host=self.host_url,
            version=version,
            previous_version=previous_version,
            latest_version=latest_version,
        )

    def initial_version(self, version=None, previous_version=None, latest_version=None):
        return self.initial_version_template.format(
            host=self.host_url,
            version=version,
            previous_version=previous_version,
            latest_version=latest_version,
        )

    def unreleased_changes(self, version=None, previous_version=None, latest_version=None):
        return self.unreleased_changes_template.format(
            host=self.host_url,
            version=version,
            previous_version=previous_version,
            latest_version=latest_version,
        )