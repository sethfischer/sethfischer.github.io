#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os


AUTHOR = u'Seth Fischer'
SITENAME = u'sethfischer'
SITEURL = ''

PATH = 'content'

DEFAULT_DATE_FORMAT = '%d %B %Y'
TIMEZONE = 'Pacific/Auckland'

DEFAULT_LANG = u'en'

TAGS_URL = 'tags.html'
CATEGORIES_URL = 'categories.html'

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
    'files',
    'images',
    'extra/CNAME',
    'extra/googledce9df78937f634a.html',
    'extra/humans.txt',
    'extra/robots.txt',
]

EXTRA_PATH_METADATA = {
    'extra/CNAME': {'path': 'CNAME'},
    'extra/googledce9df78937f634a.html': {'path': 'googledce9df78937f634a.html'},
    'extra/humans.txt': {'path': 'humans.txt'},
    'extra/robots.txt': {'path': 'robots.txt'},
}

READERS = {"html": None}

MD_EXTENSIONS = [
    'toc',
    'codehilite(css_class=highlight)',
    'extra',
]

PLUGIN_PATHS = [
    os.path.join(os.environ.get('HOME'), 'projects/pelican-plugins')
]
PLUGINS = ['assets', 'sitemap', 'pelican_githubprojects']

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 1,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

ASSET_BUNDLES = (
    ('css_bundle', [
        'css/bootstrap-custom.css',
        'css/font-custom.css',
        'css/sidebar.css',
        'css/style.css',
        'css/pygments/native.css',
    ], {}),
    ('js_bundle', [
        'js/jquery/jquery-custom.min.js',
        'js/bootstrap/transition.js',
        'js/bootstrap/collapse.js',
    ], {}),
)

THEME = os.path.join(os.environ.get('HOME'), 'projects/pelican-bootstrap3')
CUSTOM_CSS = 'static/custom.css'

CC_LICENSE_DERIVATIVES = 'Yes'
CC_LICENSE_COMMERCIAL = 'Yes'
CC_ATTR_MARKUP = False

SHOW_DATE_MODIFIED = True
DISPLAY_TAGS_ON_SIDEBAR = True
DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
GITHUB_USER = 'sethfischer'
GITHUB_SHOW_USER_LINK = True
GITHUB_REPO_URL = 'https://github.com/sethfischer/sethfischer.github.io'

