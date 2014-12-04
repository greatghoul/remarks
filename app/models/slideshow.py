import base64
from urllib import urlopen
from github import GitHub
from helpers.slide_helper import slide_meta

class Slideshow():
    def __init__(self, source_info):
        self.source_info = source_info
        self.api = GitHub()

    @classmethod
    def load(cls, source_info):
        if source_info['type'] == 'gist':
            return GistSlideshow(source_info).load()
        elif source_info['type'] == 'repo':
            return RepoSlideshow(source_info).load()

    @property
    def meta(self):
        return slide_meta(self.source)

    @property
    def title(self):
        return self.meta.get('title', '')

class GistSlideshow(Slideshow):
    def load(self):
        self.gist = self.api.gists(self.source_info['gist']).get()
        return self

    @property
    def source(self):
        return self.gist.get('files', {}).get('slide.md', {}).get('content', '')
        

class RepoSlideshow(Slideshow):
    def load(self):
        self.repo = self.api.repos(self.source_info['user'])(self.source_info['repo']).contents('%s/slide.md' % self.source_info['path']).get()
        return self

    @property
    def source(self):
        return base64.b64decode(self.repo.get('content', '')).decode('utf-8')
