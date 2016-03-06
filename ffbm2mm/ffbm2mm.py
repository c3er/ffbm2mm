#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Transform Firefox bookmarks in JSON format to a mind map in Freeplane
format.
"""


import sys
import os
import json
import re


class MMNode:
    def __init__(self, json_obj, is_root=True):
        self._json_obj = json_obj
        self.is_root = is_root
        self.text = self._get_text(json_obj)
        self.link = self._get_link(json_obj)
        self.children = self._get_children(json_obj)

    def dump(self):
        nodestr = '<node TEXT="{}"'.format(self.text)

        if self.link:
            nodestr += ' LINK="{}"'.format(self.link)

        if self.children:
            nodestr += '>\n'
            childlist = []
            for child in self.children:
                childlist.append(child.dump())
            children = "\n".join(childlist)
            nodestr += "\n".join((children, '</node>'))
        else:
            nodestr += '/>'

        if self.is_root:
            return "\n".join((
                '<map version="freeplane 1.2.0">',
                nodestr,
                '</map>'
            ))

        return nodestr

    @staticmethod
    def _get_text(obj):
        text = obj["title"]
        if text:
            # XXX Transform special characters to XML entities
            return text
        else:
            return "UNKNOWN"

    @staticmethod
    def _get_link(obj):
        try:
            uri = obj["uri"]
            if validate_url(uri):
                return uri
        except KeyError:
            pass
        return None

    @staticmethod
    def _get_children(obj):
        children = []
        try:
            json_children = obj["children"]
            for json_child in json_children:
                children.append(MMNode(json_child, False))
        except KeyError:
            pass
        return children


def validate_url(url):
    # http://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
    regex = re.compile(
        r'^(?:http|ftp)s?://'                                                                # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|'                                                                        #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'                                               # ...or ip
        r'(?::\d+)?'                                                                         # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(regex.match(url))


def error(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)


def parse_args(args):
    if len(args) != 3:
        error("Parameters: <bookmarks file name> <mind map file name>")
    bookmarks_fname = args[1]
    mm_fname = args[2]
    if not os.path.exists(bookmarks_fname):
        error("Could not find bookmarks file: " + bookmarks_fname)
    return bookmarks_fname, mm_fname


def main(args):
    bookmarks_fname, mm_fname = parse_args(args)
    with open(bookmarks_fname) as f:
        bookmarks = json.load(f)
    mm = MMNode(bookmarks)
    with open(mm_fname, "w") as f:
        f.write(mm.dump())


if __name__ == "__main__":
    main(sys.argv)