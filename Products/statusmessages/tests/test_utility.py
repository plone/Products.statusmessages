import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase

from Products.statusmessages.tests.utils import setupBrowserIdManager

app = ZopeTestCase.app()
setupBrowserIdManager(app)

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
        context = self.app
        
        util.addStatusMessage(context, u'test', type=u'info')
        test = util.showStatusMessages(context)[0]
        self.failUnless(test.message == u'test')
        self.failUnless(test.type == u'info')

        util.addStatusMessage(context, u'test', type=u'info')
        util.addStatusMessage(context, u'test1', u'warn')
        messages = util.showStatusMessages(context)
        self.failUnless(len(messages)==2)
        self.failUnless(len(util.showStatusMessages(context))==0)
        test = messages[1]
        self.failUnless(test.message == u'test1')
        self.failUnless(test.type == u'warn')

    def beforeTearDown(self):
        placelesssetup.tearDown()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestStatusMessageUtility))
    return suite

if __name__ == '__main__':
    framework()

