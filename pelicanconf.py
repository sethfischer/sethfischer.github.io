#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from datetime import datetime


AUTHOR = "Seth Fischer"
SITENAME = "sethfischer"
SITEURL = ""


# Basic settings

PAGE_URL = "{slug}.html"
PATH = "content"
READERS = {"html": None}
STATIC_PATHS = [
    "files",
    "images",
    "extra/CNAME",
    "extra/googledce9df78937f634a.html",
    "extra/humans.txt",
    "extra/robots.txt",
]


# URL settings

PAGE_SAVE_AS = "{slug}.html"
# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True


# Time and date

DEFAULT_DATE_FORMAT = "%d %B %Y"
TIMEZONE = "Pacific/Auckland"


# Metadata

EXTRA_PATH_METADATA = {
    "extra/CNAME": {"path": "CNAME"},
    "extra/googledce9df78937f634a.html": {"path": "googledce9df78937f634a.html"},
    "extra/humans.txt": {"path": "humans.txt"},
    "extra/robots.txt": {"path": "robots.txt"},
}


# Feed settings

AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
CATEGORY_FEED_ATOM = None
FEED_ALL_ATOM = None


# Pagination

DEFAULT_PAGINATION = False


# Translations

DEFAULT_LANG = "en"
TRANSLATION_FEED_ATOM = None


# Theme

LINKS = (("Leaf OBD-II manual", "https://leaf-obd.readthedocs.io/"),)
LINKS_WIDGET_NAME = "Project sites"
MENUITEMS = (
    ("Archives", "/archives"),
    ("Categories", "/categories"),
    ("Tags", "/tags"),
    ("GitHub", "https://github.com/sethfischer"),
)
SOCIAL = (
    ("github", "https://github.com/sethfischer"),
    ("gitlab", "https://gitlab.com/sethfischer"),
)
SOCIAL_WIDGET_NAME = "Code"


# Theme Flex
# https://github.com/alexandrevicenzi/Flex

THEME = "Flex"

COPYRIGHT_NAME = AUTHOR
COPYRIGHT_YEAR = datetime.now().year
MAIN_MENU = True
SITELOGO = "images/terminal.svg"
