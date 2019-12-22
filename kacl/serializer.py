from .document import KACLDocument
from .element import KACLElement
from .version import KACLVersion
from .changes import KACLChanges

class KACLMarkdownSerializer:
    def __init__(self):
        pass

    def serialize(self, document):
        if isinstance(document, KACLDocument):
            data = [ self.__serialize_header(document.header()),
                    document.header().body() ]

            link_references = []
            for version in document.versions():
                data.extend([ self.__serialize_version(version), '' ])
                if version.has_link_reference():
                    link_references.append(self.__serialize_link_reference(version))

            data.extend(link_references)
            return '\n'.join(data)
        elif isinstance(document, KACLVersion):
            return self.__serialize_version(document)

    def __serialize_header(self, obj):
        if isinstance(obj, KACLChanges):
            return f'### {obj.title()}'
        elif isinstance(obj, KACLVersion):
            version_decorator_left = ''
            version_decorator_right = ''
            if obj.has_link_reference():
                version_decorator_left = '['
                version_decorator_right = ']'
            if obj.date():
                return f'## {version_decorator_left}{obj.version()}{version_decorator_right} - {obj.date()}'
            else:
                return f'## {version_decorator_left}{obj.version()}{version_decorator_right}'
        elif isinstance(obj, KACLElement):
            return f'# {obj.title()}'

    def __serialize_version(self, obj):
        lines = [ self.__serialize_header(obj) ]
        for title, changes in obj.sections().items():
            lines.extend([
                self.__serialize_header(changes),
                self.__serialize_list(changes.items()),
                ''
            ])

        return '\n'.join(lines).strip()

    def __serialize_list(self, obj):
        lines = [ f'- {x}' for x in obj ]
        return '\n'.join(lines)

    def __serialize_link_reference(self, obj):
        return f'[{obj.version()}]: {obj.link()}'