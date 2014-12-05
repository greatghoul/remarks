from unittest import TestCase
from remarks.helpers import slide_meta

class TestHelpers(TestCase):
    def test_slide_meta(self):
        content = open('tests/fixtures/slide.md').read()
        meta = slide_meta(content)
        self.assertEqual(meta['title'], 'Introduce Remarks')

    # def test_is_slide_asset(self):
    #     self.assertTrue(is_slide_asset('greatghoul/remarks/repo.png'))
    #     self.assertTrue(is_slide_asset('greatghoul/remarks/repo.css'))
    #     self.assertTrue(is_slide_asset('greatghoul/remarks/repo/1.js'))
    #     self.assertFalse(is_slide_asset('greatghoul/remarks/repo/1'))
    #     self.assertFalse(is_slide_asset('greatghoul/repo.jpg'))

    #     self.assertTrue(is_slide_asset('gist/c2fab58e798a91a736a4/repo.PNG'))
    #     self.assertFalse(is_slide_asset('gist/c2fab58e798a91a736a4/1'))
