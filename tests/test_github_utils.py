from unittest import TestCase

from utils.github_utils import source_type, source_info

class TestGithubUtils(TestCase):

    def test_source_type(self):
        self.assertEqual(source_type('greatghoul/slides/remarks'), 'repo')
        self.assertEqual(source_type('greatghoul/slides/remarks/v1'), 'repo')
        self.assertEqual(source_type('greatghoul/63732627262'), 'gist')

    def test_get_repo_info_from_given_path(self):
        repo = source_info('greatghoul/slides/remarks')
        self.assertEqual(repo['user'], 'greatghoul')
        self.assertEqual(repo['repo'], 'slides')
        self.assertEqual(repo['path'], 'remarks')

        repo = source_info('greatghoul/slides/remarks/v1')
        self.assertEqual(repo['user'], 'greatghoul')
        self.assertEqual(repo['repo'], 'slides')
        self.assertEqual(repo['path'], 'remarks/v1')
