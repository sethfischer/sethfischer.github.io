#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = "Seth Fischer"
SITENAME = "sethfischer"
SITEURL = ""

PATH = "content"
PAGE_SAVE_AS = "{slug}.html"
PAGE_URL = "{slug}.html"

DEFAULT_DATE_FORMAT = "%d %B %Y"
TIMEZONE = "Pacific/Auckland"

DEFAULT_LANG = "en"

TAGS_URL = "tags.html"
CATEGORIES_URL = "categories.html"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

LINKS = (("Nissan Leaf OBD-II manual", "https://leaf-obd.readthedocs.io/"),)

# Social widget
SOCIAL = (
    ("GitHub", "https://github.com/sethfischer"),
    ("Code snippets", "https://gist.github.com/sethfischer"),
)
SOCIAL_WIDGET_NAME = "Code"

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

STATIC_PATHS = [
    "files",
    "images",
    "extra/CNAME",
    "extra/googledce9df78937f634a.html",
    "extra/humans.txt",
    "extra/robots.txt",
]

EXTRA_PATH_METADATA = {
    "extra/CNAME": {"path": "CNAME"},
    "extra/googledce9df78937f634a.html": {"path": "googledce9df78937f634a.html"},
    "extra/humans.txt": {"path": "humans.txt"},
    "extra/robots.txt": {"path": "robots.txt"},
}

READERS = {"html": None}

MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.codehilite": {"css_class": "highlight"},
        "markdown.extensions.extra": {},
        "markdown.extensions.toc": {},
    },
    "output_format": "html5",
}
