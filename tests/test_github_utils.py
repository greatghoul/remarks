from unittest import TestCase

from utils.github_utils import source_type

class TestGithubUtils(TestCase):

    def test_source_type(self):
        self.assertEqual(source_type('greatghoul/slides/remarks'), 'repo')
        self.assertEqual(source_type('greatghoul/slides/remarks/v1'), 'repo')
        self.assertEqual(source_type('greatghoul/63732627262'), 'gist')
