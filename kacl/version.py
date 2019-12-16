class Version:
    def __init__(self):
        self.added = []
        self.fixed = []
        self.deprecated = []
        self.removed = []
        self.fixed = []
        self.security = []
        self.date = None
        self.version = None


    def add(self, section, change):
        # getattr -> section_lower -> append()