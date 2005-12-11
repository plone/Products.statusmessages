import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase

from zope.app import zapi
from zope.app.tests import placelesssetup

from Products.Five import zcml
from Products.statusmessages.interfaces import IStatusMessageUtility
from Products.statusmessages.message import Message
from Products.statusmessages.utility import utility
import Products.statusmessages

class TestStatusMessageUtility(ZopeTestCase.ZopeTestCase):

    def afterSetUp(self):
        placelesssetup.setUp()
        zcml.load_config('meta.zcml', Products.Five)
        zcml.load_config('configure.zcml', Products.statusmessages)

    def testUtilityLookup(self):
        util = zapi.getUtility(IStatusMessageUtility)
        self.failUnless(IStatusMessageUtility.providedBy(util))

    def testUtility(self):
        util = zapi.getUtility(IStatusMessageUtility)
        request = self.app.REQUEST
        
        util.addStatusMessage(request, 'test', type='info')
        test = util.getStatusMessages(request)[0]
        self.failUnless(test.message == 'test')
        self.failUnless(test.type == 'info')

        util.addStatusMessage(request, 'test1', 'warn')
        messages = util.showStatusMessages(request)
        self.failUnless(len(messages)==2)
        self.failUnless(len(util.getStatusMessages(request))==0)
        test = messages[1]
        self.failUnless(test.message == 'test1')
        self.failUnless(test.type == 'warn')
        
        util.addStatusMessage(request, 'test2', 'stop')
        self.failUnless(len(util.getStatusMessages(request))==1)
        util.clearStatusMessages(request)
        self.failUnless(len(util.getStatusMessages(request))==0)

    def beforeTearDown(self):
        placelesssetup.tearDown()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestStatusMessageUtility))
    return suite

if __name__ == '__main__':
    framework()

