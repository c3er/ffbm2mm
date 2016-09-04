#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Transform Firefox bookmarks in JSON format to a mind map in Freeplane
format.
"""


import sys
import os
import re
import string
import collections
import json
import xml.sax.saxutils as sax


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
        try:
            text = obj["title"]
            if text:
                return escape2xml(text)
        except KeyError:
            pass
        return "UNKNOWN"

    @staticmethod
    def _get_link(obj):
        try:
            uri = obj["uri"]
            if validate_url(uri):
                return sax.escape(uri)
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


# Helpers #####################################################################

def escape2xml(text):
    tmp = sax.escape(text)
    charlist = list(tmp)
    for i, char in enumerate(charlist):
        if char not in string.printable:
            charlist[i] = "&#x" + hex(ord(char))[2:] + ";"
    return "".join(charlist)


def validate_url(url):
    # http://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
    regex = re.compile(
        r'^(?:http|ftp)s?://'                                                                # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|'                                                                        #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'                                               # ...or ip
        r'(?::\d+)?'                                                                         # optional port
        r'(?:/?|[/?]\S+)$',
        re.IGNORECASE
    )
    return bool(regex.match(url))

###############################################################################


def error(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)


# Helpers used by main function ###############################################

def parse_args(args):
    if len(args) != 3:
        error("Parameters: <bookmarks file name> <mind map file name>")
    bookmarks_fname = args[1]
    mm_fname = args[2]
    if not os.path.exists(bookmarks_fname):
        error("Could not find bookmarks file: " + bookmarks_fname)
    return bookmarks_fname, mm_fname

###############################################################################


def main(args):
    bookmarks_fname, mm_fname = parse_args(args)
    with open(bookmarks_fname, encoding="utf8") as f:
        bookmarks = json.load(f, object_pairs_hook=collections.OrderedDict)
    mm = MMNode(bookmarks)
    with open(mm_fname, "w") as f:
        f.write(mm.dump())


if __name__ == "__main__":
    main(sys.argv)