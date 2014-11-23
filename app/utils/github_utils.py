""" Github Utilities
"""

import re

PATTERN_REPO_URL = r'(?P<user>[^\/]+)\/(?P<repo>[^\/]+)\/(?P<path>\S+)'
PATTERN_GIST_URL = r'(?P<user>[^\/]+)\/(?P<gist>[^\/]+)'

def source_type(path):
    """ Detect if a given path stands for a repo path or a gist path
    """
    if re.match(PATTERN_REPO_URL, path):
        return 'repo'
    elif re.match(PATTERN_GIST_URL, path):
        return 'gist'
    else:
        return None

def source_info(path):
    """ Extract source info from given path

    If given a repo path, returns user, repo and path in hash
    If given a gist path, returns user, gist in hash
    """

    the_source_type = source_type(path)
    if the_source_type == 'repo':
        return re.match(PATTERN_REPO_URL, path).groupdict()
    elif the_source_type == 'gist':
        return re.match(PATTERN_GIST_URL, path).groupdict()

    return {}
