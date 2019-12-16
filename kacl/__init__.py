from .parser import *



def load(file):
    """
    Parse the first YAML document in a stream
    and produce the corresponding Python object.
    """
    file_stream = open(file, 'r')

    parser = Parser(file_stream)
    try:
        return parser.parse()
    finally:
        parser.dispose()

def parse(stream):
    pass