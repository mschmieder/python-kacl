from .element import KACLElement

import re

class KACLParser:
    semver_regex = r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?'

    @staticmethod
    def parse_header(text, start_depth, end_depth=None, line_offset=0):
        if not end_depth:
            end_depth = start_depth

        elements = []
        reg_expr_start = r'(\n{depth}|^{depth})\s+?(.*)\n'.format(depth="#"*start_depth)
        reg_expr_end = r'(\n{depth}|^{depth})\s+?(.*)\n'.format(depth="#"*end_depth)
        for match in re.finditer(reg_expr_start, text):
            # find end of section
            raw = match.group().strip()
            title = match.group(2).strip()
            start = match.start()
            end = match.end()
            line_number = text[:start].count('\n')+line_offset
            if match.group()[0] == '\n':
                line_number += 2
            else:
                line_number += 1

            next_match = re.search(reg_expr_end, text[end:])
            body = None
            if next_match:
                body = text[end:next_match.start()+end]
            else:
                body = text[end:]
            elements.append(KACLElement(raw=raw, title=title,
                                        body=body, line_number=line_number))

        return elements

    @staticmethod
    def parse_link_references(text):
        link_references = dict()
        begin = None
        reg_expr = r'\n\[(.*)\]:(.*)'
        for match in re.finditer(reg_expr, text):
            if begin is None:
                begin = match.start()
            version = match.group(1).strip()
            link = match.group(2).strip()
            line_number = text[:match.start()].count('\n')+1
            link_references[version] = KACLElement(raw=match.group().strip(), title=version, body=link, line_number=line_number)

        return begin, link_references

    @staticmethod
    def parse_sem_ver(text, regex=None):
        if regex == None:
            regex = KACLParser.semver_regex
        m = re.search(regex, text)
        if m:
            return m.group().strip()
