import re
import json
import urllib2
import urlparse

SOURCE_PATTERNS = {
    'repo': r'(?P<user>[^\/\s]+)\/(?P<path>\S+)',
    'gist': r'(?P<gist>[0-9A-Za-z]{20})'
}

def source_info(path):
    """ Detect if a given path stands for a repo path or a gist path
    """

    for source_type, path_pattern in SOURCE_PATTERNS.items():
        match = re.match(path_pattern, path)
        if match:
            info = dict(match.groupdict(), type=source_type)
            if source_type == 'repo':
                info['repo'] = 'slides'
            return info

    return None

def slide_meta(content):
    metadata = {}
    frontmatter = re.sub(r'\s*^---.*$[\s\S]*', '', content, flags=re.M)
    for line in frontmatter.split('\n'):
        key, val = re.split(r':\s*', line, maxsplit=1)
        metadata[key] = val
        
    return metadata
