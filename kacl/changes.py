from .parser import KACLParser
from .element import KACLElement
import re


class KACLChanges(KACLElement):
    def __init__(self, element):
        KACLElement.__init__(self, 
                             raw=element.raw(),
                             title=element.title(),
                             body=element.body(),
                             line_number=element.line_number())
        self.__items = []

    def items(self):
        if not len(self.__items) and len(self.body().strip()):
            body = self.body()
            items = ("\n"+body).split('\n-')
            self.__items = [x.strip() for x in items if len(x.strip()) > 0]
        return self.__items

    def add(self, item):
        self.items().append(item)
