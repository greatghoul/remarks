import base64
import json
from urllib import urlopen
from github import GitHub
from sae.kvdb import KVClient
from remarks.helpers import slide_meta

api = GitHub()
kvdb = KVClient()

class Slideshow():
    @classmethod
    def gist(cls, gist):
        return GistSlideshow(gist).load()
    
    @classmethod
    def repo(cls, user, path):
        return RepoSlideshow(user, path).load()

    @property
    def meta(self):
        return slide_meta(self.source)

    @property
    def title(self):
        return self.meta.get('title', '')

class GistSlideshow(Slideshow):
    def __init__(self, gist):
        self.gist = gist
        self._key = str('gist/%s' % gist)

    def load(self):
        return self

    def file(self, filename):
        if filename == 'slide.md':
            self.response = api.gists(self.gist).get()
            kvdb.set(self._key, json.dumps(self.response))
        else:
            self.response = json.loads(kvdb.get(self._key))

        return self.response.get('files', {}).get(filename, {})

    def file_content(self, filename):
        return self.file(filename).get('content', '')

    def file_url(self, filename):
        return self.file(filename).get('raw_url', '')

    @property
    def source(self):
        return self.file('slide.md').get('content', '')
        

class RepoSlideshow(Slideshow):
    def __init__(self, user, slug):
        self.user = user
        self.slug = slug
        self.repo = 'slides'

    def file(self, filename):
        full_filename = '%s/%s' % (self.slug, filename)
        return api.repos(self.user)(self.repo).contents(full_filename).get()

    def file_content(self, filename):
        return base64.b64decode(self.file(filename).get('content', '')).decode('utf-8')

    def file_url(self, filename):
        full_filename = '%s/%s/master/%s/%s' % (self.user, self.repo, self.slug, filename)
        return 'https://raw.github.com/%s' % full_filename

    def load(self):
        return self

    @property
    def source(self):
        return self.file_content('slide.md')
