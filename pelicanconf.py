#!/usr/bin/env python

from datetime import datetime

AUTHOR = "Seth Fischer"
SITENAME = "Seth Fischer"
SITESUBTITLE = "Software Engineer"
SITEURL = ""


# Basic settings

PAGE_URL = "{slug}.html"
PATH = "content"
READERS = {"html": None}
STATIC_PATHS = [
    "static",
]


# URL settings

PAGE_SAVE_AS = "{slug}.html"
# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True


# Time and date

DEFAULT_DATE_FORMAT = "%-d %B %Y"
LOCALE = "en_NZ.UTF-8"
TIMEZONE = "Pacific/Auckland"


# Metadata

DEFAULT_METADATA = {
    "status": "draft",
}
EXTRA_PATH_METADATA = {
    "static/extra/CNAME": {"path": "CNAME"},
    "static/extra/googledce9df78937f634a.html": {"path": "googledce9df78937f634a.html"},
    "static/extra/humans.txt": {"path": "humans.txt"},
    "static/extra/robots.txt": {"path": "robots.txt"},
}


# Feed settings

AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
CATEGORY_FEED_ATOM = None
FEED_ALL_ATOM = None


# Translations

DEFAULT_LANG = "en"
TRANSLATION_FEED_ATOM = None


# Theme

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

# Theme Flex
# https://github.com/alexandrevicenzi/Flex

THEME = "Flex"

COPYRIGHT_NAME = AUTHOR
COPYRIGHT_YEAR = datetime.now().year
CUSTOM_CSS = "static/css/flex-custom.css"
MAIN_MENU = True
OG_LOCALE = "en_GB"
ROBOTS = "index, follow"
SITELOGO = "/static/icons/terminal.svg"
SITETITLE = SITENAME
