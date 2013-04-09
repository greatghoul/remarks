# -*- coding: utf-8 -*-
"""
    Utilities to fetch content from github 
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    A set of helper functions used for remarks.
"""

from log import log
from github import GitHub
import re, json, urllib2, urlparse

gh = GitHub()

def get_gist_by_url(url):
    """ Get gist info from given url. """

    gist_id  = urlparse.urlsplit(url).geturl().split('/')[-1]
    return gh.gists(gist_id).get()


def get_slides_source_from_gist(gist):
    """ Get remark style slides's markdown source

    First, remarks will search for file ``slides.md`` and return its content
    
    If file ``slides.md`` does not exists, remarks will scan files like slide1.md, slide2.md, slide3.md ...
    If slide files found, remark will join each of their content with ``---`` and return.
    (``---`` is the slide separater for `remark <https://github.com/gnab/remark>`_ )
   
    If no slides.md or slideN.md found, None will be return instead.
    """
    
    log.info('Guessing slides.md source')
    slides_file = gist.get('files', {}).get('slides.md', None)
    if slides_file:
        log.info('slides.md found.')
        return slides_file.get('content', '')
    
    log.info('Guessing slideN.md sources')
    slide_files = [v for k, v in gist.get('files', {}).items() if re.match(r'slide\d+\.md', k)]
    slide_files = sorted(slide_files, key=lambda slide_file: int(re.sub(r'\D', '', slide_file.get('filename', ''))))
    if slide_files:
        log.info('%d slideN.md files found', len(slide_files))
        return '\n---\n'.join([slide_file.get('content', '') for slide_file in slide_files])

    log.warn('No slides found')
    return None 

