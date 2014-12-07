#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os


AUTHOR = u'Seth Fischer'
SITENAME = u'sethfischer'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Pacific/Auckland'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = None

# Social widget
SOCIAL = (
    ('GitHub', 'https://github.com/sethfischer'),
    ('Bitbucket', 'https://bitbucket.org/sethfischer'),
    ('Drupal', 'https://drupal.org/u/sethfischer'),
)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

STATIC_PATHS = [
    'images',
    'extra/CNAME',
    'extra/googledce9df78937f634a.html',
    'extra/humans.txt',
    'extra/robots.txt',
    'extra/custom.css',
]

EXTRA_PATH_METADATA = {
    'extra/CNAME': {'path': 'CNAME'},
    'extra/googledce9df78937f634a.html': {'path': 'googledce9df78937f634a.html'},
    'extra/humans.txt': {'path': 'humans.txt'},
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/custom.css': {'path': 'static/custom.css'},
}

READERS = {"html": None}

MD_EXTENSIONS = [
    'toc',
    'codehilite(css_class=highlight)',
    'extra',
]

THEME = os.path.join(os.environ.get('HOME'), 'projects/pelican-bootstrap3')
CUSTOM_CSS = 'static/custom.css'
CC_LICENSE = 'CC-BY'
DISPLAY_TAGS_ON_SIDEBAR = False
DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
GITHUB_USER = 'sethfischer'
GITHUB_SHOW_USER_LINK = True

