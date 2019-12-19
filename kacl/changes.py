from .parser import KACLParser
from .element import KACLElement
import re


class KACLChanges(KACLElement):
    def __init__(self, element):
        KACLElement.__init__(self, title=element.title(), body=element.body(), start=element.start(), end=element.end(), )
        self.__items = None

    def items(self):
        if self.__items:
            return self.__items
        else:
            body = self.body()

            # first bring order into the chaos by bringing all items into one line
            #clean_body = re.sub(r'\n\s+', '', body)
            items = ("\n"+body).split('\n-')
            self.__items = [ x.strip() for x in items if len(x.strip()) > 0 ]
        return self.__items


