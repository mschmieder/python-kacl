from .element import KACLElement

import re
import markdown

class KACLParser:
    @staticmethod
    def parse_header(text, depth):
        elements = []
        reg_expr = r'(\n{depth}|^{depth})\s+(.*)\n'.format(depth="#"*depth)

        for match in re.finditer(reg_expr, text):
            # find end of section
            title = match.group(2).strip()
            start = match.start()
            end   = match.end()

            next_match = re.search(reg_expr, text[end:])
            body = None
            if next_match:
                body = text[end:next_match.start()+end]
            else:
                end = len(text)
                body = text[end:]

            print(body)

            elements.append( KACLElement(title=title, body=body, start=start, end=end) )

        return elements