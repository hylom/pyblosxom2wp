#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""pyblosxom2wp.py: generate XML to import pyblosxom stroy to WordPress."""

import sys
import os.path
import dircache
import time
import re
import wordpress

from BeautifulSoup import BeautifulStoneSoup

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
        self._wxr = wordpress.WordPressWxr()
        self._wxr.channel = wordpress.Channel(
            title = "dailyhckr",
            link = "http://hylom.net/",
            base_blog_url = "http://hylom.net/",
            pubDate = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()),
            language = "ja")

    def convert(self):
        """do convert"""
        self.scan_dir(self._story_dir)
        print self._wxr.WriteXml()


    def read_text(self, filepath):
        """read textfile and returns categories, tags, title, content"""
        f = open(filepath, "r")
        if not f:
            print >> sys.stderr, "cannot open: %s. skipping...\n" % filepath
            return None

        title = f.readline().strip()

        next = f.readline()
        tags = []
        while next[0] == "#":
            if next[0:4] == "#tag":
                tags = next[4:].split()
            next = f.readline()

        content = next + f.read()
        f.close()
        return (tags, title, content)


    def get_categories(self, path):
        """get categories from path"""
        rpath = os.path.relpath(path, self._story_dir)
        (rdir, fname) = os.path.split(rpath)
        return rdir.split(os.path.sep)

    def escape(self, match):
        xml = match.group(0)

        if xml.find("\001") != -1:
            print >> sys.stderr, "invalid character: \\001."
        if xml.find("\002") != -1:
            print >> sys.stderr, "invalid character: \\002."
        if xml.find("\003") != -1:
            print >> sys.stderr, "invalid character: \\003."

        xml = xml.replace(" ", "\001");
        xml = xml.replace("\t", "\002");
        xml = xml.replace("\n", "\003");
        
        return xml

    def unescape(self, xml):
        xml = xml.replace("\001", " ");
        xml = xml.replace("\002", "\t");
        xml = xml.replace("\003", "\n");
        
        return xml


    def text_to_xml_item(self, filepath):
        """read file and generate xml"""
        pname = os.path.basename(filepath).replace(".txt", "")
        date = os.path.getmtime(filepath)
        (tags, title, content) = self.read_text(filepath)  # TODO: do exception proc.
        categories = self.get_categories(filepath)
        date_str = time.strftime( "%Y-%m-%d %H:%M:%S", time.localtime(date) );
        date_str_gmt = time.strftime( "%Y-%m-%d %H:%M:%S", time.gmtime(date) );
        pubDate_str = time.strftime( "%a, %d %b %Y %H:%M:%S +0000", time.gmtime(date) );
        tidied = content
        tidied = tidied.replace("\r\n", "\n")
        
        rex = re.compile(r"<pre>.*?</pre>", re.S)
        tidied = rex.sub(self.escape, tidied)

        tidied = BeautifulStoneSoup(tidied).prettify()
        tidied = tidied.replace("\n", "")
        tidied = tidied.replace(",", "&#44;")
        tidied = self.unescape(tidied)
        
        # add entry
        post_item = wordpress.Item(
            title = title,
            pubDate = pubDate_str,
            post_date = date_str,
            post_date_gmt = date_str_gmt,
            content = tidied,
            post_name = pname)
        post_item.tags = tags
        post_item.categories = categories
        self._wxr.channel.items.append(post_item)

    def scan_dir(self, dir):
        """scan dir and proccess"""

        # get files
        files = dircache.listdir(dir)
        for file in files:
            path = os.path.join(dir, file)
            if os.path.isdir(path):
                self.scan_dir(path)
            else:
                self.text_to_xml_item(path)


main()

