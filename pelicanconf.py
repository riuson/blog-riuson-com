#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Vladimir'
SITENAME = 'riuson.com'
SITEURL = ''
DEFAULT_LANG = 'ru'
LOCALE = 'ru_RU'

PATH = 'content'

TIMEZONE = 'Asia/Yekaterinburg'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

USE_FOLDER_AS_CATEGORY = False
DEFAULT_CATEGORY = 'misc'
DISPLAY_CATEGORIES_ON_MENU = False

ARTICLE_URL          = '{lang}/posts/{date:%Y}/{date:%m}/{date:%d}/{slug}'
ARTICLE_LANG_URL     = '{lang}/posts/{date:%Y}/{date:%m}/{date:%d}/{slug}'
ARTICLE_SAVE_AS      = '{lang}/posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
ARTICLE_LANG_SAVE_AS = '{lang}/posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
PAGE_URL             = '{lang}/{slug}'
PAGE_LANG_URL        = '{lang}/{slug}'
PAGE_SAVE_AS         = '{lang}/{slug}/index.html'
PAGE_LANG_SAVE_AS    = '{lang}/{slug}/index.html'

LOAD_CONTENT_CACHE = False
DATE_FORMATS = {
    'en': '%a, %d %b %Y',
    'ru': '%d %B %Y г., %a',
}
ARTICLE_PATHS = ['articles']
PAGES_PATHS = ['pages']
THEME = 'theme'
STATIC_PATHS = ['images', 'redirects']
FILENAME_METADATA = r'^(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.*)-(?P<lang>\w{2})$'
SUMMARY_MAX_LENGTH = 10
MARKDOWN = {
    'extensions' : ['markdown.extensions.codehilite'],
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.fenced_code': {},
        'markdown.extensions.attr_list': {},
    }
}

EXTRA_PATH_METADATA = {
    'redirects/lcd-image-converter.html': {'path': 'lcd-image-converter/index.html'}
}

#PLUGIN_PATHS = ["../pelican-plugins"]
#PLUGINS = ["i18n_subsites"]
#I18N_SUBSITES = {
#  'en': { 
#    'SITENAME': 'riuson.com',
#    'LOCALE': 'en_US',            #This is somewhat redundant with DATE_FORMATS, but IMHO more convenient
#  },
#  'ru': { 
#    'SITENAME': 'riuson.com',
#    'LOCALE': 'ru_RU',            #This is somewhat redundant with DATE_FORMATS, but IMHO more convenient
#  },
#}
#I18N_UNTRANSLATED_ARTICLES = 'remove'
#I18N_UNTRANSLATED_PAGES = 'remove'
