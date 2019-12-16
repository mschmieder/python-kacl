class KACLDocument:
    def __init__(self, content):
        self.content = content
        self.description = None
        self.versions = []

    def validate(self):
        pass

    def add(self, section, content):
        pass

    def release(self, version):
        pass

    def get(self, version):
        pass

    def dump(self, file=None):
        pass