#!/usr/bin/env python
 
import unittest
import sys
import os

# Extend path to load app modules in tests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

if __name__ == '__main__':
    all_tests = unittest.TestLoader().discover('tests', pattern='test_*.py')
    unittest.TextTestRunner().run(all_tests)