import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from unittest import TestSuite
from Testing.ZopeTestCase import ZopeDocTestSuite

def test_suite():
    return TestSuite((
        ZopeDocTestSuite('Products.statusmessages.utility'),
        ZopeDocTestSuite('Products.statusmessages.message'),
    ))

if __name__ == '__main__':
    framework()

