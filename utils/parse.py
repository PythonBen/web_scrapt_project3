from selectolax.parser import Node, HTMLParser
from typing import Union
def parse_raw_attribute(node: Union[Node, str], selectors: list[dict]):

    if not issubclass(Node, type(node)):
        node = HTMLParser(node)
    parsed = {}

    for s in selectors:
        match = s.get("match")
        type_ = s.get("type")
        selector = s.get("selector")
        name = s.get("name")

        if match == "all":
            matched = node.css(selector)
            if type_ == "text":
                parsed[name] = [node.text() for node in matched]
            elif type_ == "node":
                parsed[name] = matched

        elif match == "first":
            matched = node.css_first(selector)

            if type_ == "text":
                parsed[name] = matched.text()
            elif type_ == "node":
                parsed[name] = matched

    return parsed

