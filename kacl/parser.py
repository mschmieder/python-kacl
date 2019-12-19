from .element import KACLElement

import re
import markdown

class KACLParser:
    @staticmethod
    def parse_header(text, start_depth, end_depth=None):
        if not end_depth:
            end_depth = start_depth

        elements = []
        reg_expr_start = r'(\n{depth}|^{depth})\s+(.*)\n'.format(depth="#"*start_depth)
        reg_expr_end   = r'(\n{depth}|^{depth})\s+(.*)\n'.format(depth="#"*end_depth)
        for match in re.finditer(reg_expr_start, text):
            # find end of section
            title = match.group(2).strip()
            start = match.start()
            end   = match.end()

            next_match = re.search(reg_expr_end, text[end:])
            body = None
            if next_match:
                body = text[end:next_match.start()+end]
            else:
                body = text[end:]
            elements.append( KACLElement(title=title, body=body, start=start, end=end) )

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
            link_references[version] = link

        return begin, link_references

    @staticmethod
    def parse_sem_ver(text):
        semver_regex = r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?'
        m = re.search(semver_regex, text)
        if m:
            return m.group().strip()