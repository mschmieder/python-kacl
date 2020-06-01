# Version of the python-kacl package
__version__ = "0.2.20"

from .document import *
from .serializer import *

def load(file):
    """
    Parse the first YAML document in a stream
    and produce the corresponding Python object.
    """
    doc = None
    with open(file, 'r') as f:
        document = f.read()
        try:
            doc = KACLDocument.parse(document)
        finally:
            f.close()
    return doc

def parse(text):
    return KACLDocument.parse(text)

def dump(document):
    return KACLMarkdownSerializer().serialize(document)

def new():
    return KACLDocument.init()