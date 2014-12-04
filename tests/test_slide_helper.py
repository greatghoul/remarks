from unittest import TestCase
from helpers.slide_helper import source_info, slide_meta

class TestSlideHelper(TestCase):
    def setUp(self):
        self.gist_path = 'greatghoul/c2fab58e798a91a736a4'
        self.repo_path = 'greatghoul/slides/remarks'
        self.repov1_path = 'greatghoul/slides/remarks/v1'
        self.invalid_paths = [
            '/greatghoul/slides',
            'gre atghoul/ slides',
            '/greatghoul',
            'greatghoul',
        ]

    def test_extract_gist_info_from_path(self):
        gist = source_info(self.gist_path)
        self.assertEqual(gist['type'], 'gist')
        self.assertEqual(gist['user'], 'greatghoul')
        self.assertEqual(gist['gist'], 'c2fab58e798a91a736a4')

    def test_extract_repo_info_from_path(self):
        repo = source_info(self.repo_path)
        self.assertEqual(repo['type'], 'repo')
        self.assertEqual(repo['user'], 'greatghoul')
        self.assertEqual(repo['repo'], 'slides')
        self.assertEqual(repo['path'], 'remarks')

        repo = source_info(self.repov1_path)
        self.assertEqual(repo['type'], 'repo')
        self.assertEqual(repo['user'], 'greatghoul')
        self.assertEqual(repo['repo'], 'slides')
        self.assertEqual(repo['path'], 'remarks/v1')

    def test_invalid_source_type(self):
        for path in self.invalid_paths:
            source = source_info(path)
            self.assertIsNone(source)

    def test_slide_meta(self):
        content = open('tests/fixtures/slide.md').read()
        meta = slide_meta(content)
        self.assertEqual(meta['title'], 'Introduce Remarks')
