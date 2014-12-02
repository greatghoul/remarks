from urllib import urlopen
from pygithub3 import Github
from helpers.slide_helper import slide_meta

class Slideshow():
    def __init__(self, source_info):
        self.source_info = source_info
        self.api = Github()

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
        # self.gist = self.api.gists(self.source_info['gist']).get()
        self.gist = self.api.gists.get('ea4e72a819fe764efafc')
        return self

    @property
    def source(self):
        return self.gist.files.get('slide.md').content
        

class RepoSlideshow(Slideshow):
    def load(self):
        return self

    @property
    def source(self):
        return ""
