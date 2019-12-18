from .document import *

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

def parse(stream):
    pass