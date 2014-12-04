from unittest import TestCase
from remarks.helpers.slide_helper import source_info, slide_meta

class TestSlideHelper(TestCase):
    def test_extract_gist_info_from_path(self):
        gist = source_info('c2fab58e798a91a736a4')
        self.assertEqual(gist['type'], 'gist')
        self.assertEqual(gist['gist'], 'c2fab58e798a91a736a4')

    def test_extract_repo_info_from_path(self):
        repo = source_info('greatghoul/remarks')
        self.assertEqual(repo['type'], 'repo')
        self.assertEqual(repo['user'], 'greatghoul')
        self.assertEqual(repo['repo'], 'slides')
        self.assertEqual(repo['path'], 'remarks')

        repo = source_info('greatghoul/remarks/v1')
        self.assertEqual(repo['type'], 'repo')
        self.assertEqual(repo['user'], 'greatghoul')
        self.assertEqual(repo['repo'], 'slides')
        self.assertEqual(repo['path'], 'remarks/v1')

    def test_invalid_source_type(self):
        invalid_paths = [
            '/greatghoul/slides',
            'gre atghoul/ slides',
            '/greatghoul',
            'greatghoul',
        ]

        for path in invalid_paths:
            source = source_info(path)
            self.assertIsNone(source)

    def test_slide_meta(self):
        content = open('tests/fixtures/slide.md').read()
        meta = slide_meta(content)
        self.assertEqual(meta['title'], 'Introduce Remarks')
