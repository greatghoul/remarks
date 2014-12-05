import re
import json
import urllib2
import urlparse

def slide_meta(content):
    metadata = {}
    frontmatter = re.sub(r'\s*^---.*$[\s\S]*', '', content, flags=re.M)
    for line in frontmatter.split('\n'):
        key, val = re.split(r':\s*', line, maxsplit=1)
        metadata[key] = val
        
    return metadata