class KACLElement:
    def __init__(self, title="", body="", start=None, end=None):
        self.__title = title
        self.__body = body
        self.__start = start
        self.__end = end

    def start(self):
        return self.__start

    def end(self):
        return self.__end

    def title(self):
        return self.__title

    def body(self):
        return self.__body