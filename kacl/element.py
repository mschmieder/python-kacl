class KACLElement:
    def __init__(self, raw="", title="", body="", line_number=None):
        self.__raw = raw
        self.__title = title
        self.__body = body
        self.__line_number = line_number

    def line_number(self):
        return self.__line_number

    def title(self):
        return self.__title

    def body(self):
        return self.__body

    def raw(self):
        return self.__raw