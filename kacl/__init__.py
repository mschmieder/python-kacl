from .document import *
from .serializer import *

def load(file):
    """
    Parse the first YAML document in a stream
    and produce the corresponding Python object.
    """
    with open(file, 'r') as f:
        document = f.read()
        try:
            return KACLDocument.parse(document)
        finally:
            f.close()

def dump(document):
    return KACLMarkdownSerializer().serialize(document)