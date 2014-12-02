#!/usr/bin/env python
 
import unittest
import sys
import os

# Extend path to load app modules in tests
root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, 'app'))

if __name__ == '__main__':
    all_tests = unittest.TestLoader().discover('tests', pattern='test_*.py')
    unittest.TextTestRunner().run(all_tests)