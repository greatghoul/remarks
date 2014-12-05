import httpretty

from unittest import TestCase
from remarks.models import Slideshow

MOCKS = {
    'gist': {
        'url': 'https://api.github.com/gists/ea4e72a819fe764efafc',
        'file': 'tests/fixtures/gist.json',
    },
    'repo': {
        'url': 'https://api.github.com/repos/greatghoul/slides/contents/remarks/slide.md',
        'file': 'tests/fixtures/repo.json',
    },
}

class TestSlideshow(TestCase):

    def mock(self, name):
        info = MOCKS[name]
        body = open(info['file']).read()
        httpretty.register_uri(httpretty.GET, info['url'], body=body, content_type='application/json')

    def setUp(self):
        httpretty.enable()

    def tearDown(self):
        httpretty.disable()

    def test_load_gist_source(self):
        self.mock('gist')

        slide = Slideshow.gist('ea4e72a819fe764efafc')
        self.assertEqual(slide.source, open('tests/fixtures/slide.md').read())
        self.assertEqual(slide.title, 'Introduce Remarks')


    def test_load_repo_source(self):
        self.mock('repo')

        slide = Slideshow.repo('greatghoul', 'remarks')
        self.assertEqual(slide.source, open('tests/fixtures/slide.md').read())
        self.assertEqual(slide.title, 'Introduce Remarks')
