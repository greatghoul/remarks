""" Github Utilities
"""

import re

PATTERN_REPO_URL = r'(?P<user>[^\/]+)\/(?P<repo>[^\/]+)\/(?P<path>[^\/]+)'
PATTERN_GIST_URL = r'(?P<user>[^\/]+)\/(?P<repo>[^\/]+)'

def source_type(path):
    """ Detect if a given path stands for a repo path or a gist path
    """
    if re.match(PATTERN_REPO_URL, path):
        return 'repo'
    elif re.match(PATTERN_GIST_URL, path):
        return 'gist'
    else:
        return None
