"""
    Status messages utility tests.
"""

import unittest
from zope.testing.doctestunit import DocTestSuite

def test_suite():
    return unittest.TestSuite((
        DocTestSuite('Products.statusmessages.utility'),
        DocTestSuite('Products.statusmessages.message'),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest="test_suite")

