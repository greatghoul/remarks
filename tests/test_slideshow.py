import httpretty

from unittest import TestCase
from models import Slideshow
from helpers.slide_helper import source_info

MOCKS = {
    'gist': {
        'url': 'https://api.github.com/gists/ea4e72a819fe764efafc',
        'file': 'tests/fixtures/gist.json',
    },
}

class TestSlideshow(TestCase):

    def mock(self, name):
        info = MOCKS[name]
        body = open(info['file']).read()
        httpretty.register_uri(httpretty.GET, info['url'], body=body)

    def setUp(self):
        httpretty.enable()
        #pass

    def tearDown(self):
        httpretty.disable()
        #pass

    def test_load_gist_source(self):
        self.mock('gist')

        info = source_info('greatghoul/ea4e72a819fe764efafc')
        slide = Slideshow.load(info)
        self.assertEqual(slide.source, open('tests/fixtures/slide.md').read())
        self.assertEqual(slide.title, 'Introduce Remarks')


    def test_load_repo_source(self):
        self.mock('repo')

        info = source_info('greatghoul/slides/remarks')
        slide = Slideshow.load(info)
        self.assertEqual(slide.soruce, open('tests/fixtures/slide.md'))
        self.assertEqual(slide.title, 'Introduce Remarks')
