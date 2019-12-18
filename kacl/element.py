class KACLElement:
    def __init__(self, title, body, start, end):
        self.__title = title
        self.__body = body
        self.__start = None
        self.__end = None

    def start(self):
        return self.__start

    def end(self):
        return self.__end

    def title(self):
        return self.__title

    def body(self):
        return self.__body