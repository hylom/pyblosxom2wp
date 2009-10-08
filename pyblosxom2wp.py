#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""pyblosxom2wp.py: generate XML to import pyblosxom stroy to WordPress."""

import sys
import os.path
import dircache

"""
XML/XHTML import format of WordPress:

<item>
 <pubDate>Wed, 30 Jan 2009 12:00:00 +0000</pubDate>
 <category>Kites</category>
 <category>Taiwan</category>
 <title>Fun times</title>
 <content:encoded><p>What great times we had...</p><p>And then Bob...</p></content:encoded>
</item>
<item>...

( http://codex.wordpress.org/Importing_Content )
"""

usage = "usage: %s <pyblosxom's_story_directory>" % sys.argv[0]

# main routine
def main():
    # parse arguments
    try:
        story_dir = sys.argv[1]
    except IndexError:
        exit(usage)

    Pyblosxom2wp(story_dir).convert()


class Pyblosxom2wp(object):
    """convert pyblosxom stories to WordPress import style XML."""

    def __init__(self, story_dir):
        """initialization"""
        self._story_dir = story_dir


    def convert(self):
        """do convert"""
        self.scan_dir(self._story_dir)


    def read_text(self, filepath):
        """read textfile and returns categories, tags, title, content"""
        f = open(filepath, "r")
        if not f:
            print >> sys.stderr, "cannot open: %s. skipping...\n" % filepath
            return None

       title = f.readline()

       next = f.readline()
       tags = []
       while next[0] == "#":
           if next[0:4] == "#tag":
               tags = next[4:].split()
           next = f.readline()

       content = next + f.read()
       f.close()
       return (tags, title, content)


    def text_to_xml_item(self, filepath):
        """read file and generate xml"""
        date = getmtime(path)
        (tags, title, content) = read_text(filepath)  # TODO: do exception proc.
        categories = get_categories(filepath)

    def scan_dir(self, dir):
        """scan dir and proccess"""

        # get files
        files = dircache.listdir(dir)
        for file in files:
            path = os.path.join(story_dir, file)
            if os.path.isdir(path):
                scan_dir(path)
            else:
                text_to_xml_item(path)


main()

