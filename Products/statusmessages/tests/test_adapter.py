import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase

from zope.app import zapi
from zope.app.tests import placelesssetup

from Products.Five import zcml
from Products.statusmessages.interfaces import IStatusMessage
from Products.statusmessages.message import Message
from Products.statusmessages.adapter import StatusMessage
import Products.statusmessages, Products.statusmessages.tests

class TestStatusMessage(ZopeTestCase.ZopeTestCase):

    def afterSetUp(self):
        placelesssetup.setUp()
        zcml.load_config('meta.zcml', Products.Five)
        zcml.load_config('configure.zcml', Products.statusmessages.tests)
        zcml.load_config('configure.zcml', Products.statusmessages)

    def testAdapterLookup(self):
        status = IStatusMessage(self.app.REQUEST)
        self.failUnless(IStatusMessage.providedBy(status))

    def testAdapter(self):
        request = self.app.REQUEST
        status = IStatusMessage(request)

        # make sure there's no stored message
        self.assertEqual(len(status.showStatusMessages()), 0)

        # add one message
        status.addStatusMessage(u'test', type=u'info')
        messages = status.showStatusMessages()
        self.failUnless(len(messages)==1)
        self.failUnless(messages[0].message == u'test')
        self.failUnless(messages[0].type == u'info')

        # make sure messages are removed
        self.assertEqual(len(status.showStatusMessages()), 0)

        # add two messages
        status.addStatusMessage(u'test', type=u'info')
        status.addStatusMessage(u'test1', u'warn')
        messages = status.showStatusMessages()
        self.failUnless(len(messages)==2)
        test = messages[1]
        self.failUnless(test.message == u'test1')
        self.failUnless(test.type == u'warn')

        # make sure messages are removed again
        self.failUnless(len(status.showStatusMessages())==0)

    def beforeTearDown(self):
        placelesssetup.tearDown()

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestStatusMessage))
    return suite

if __name__ == '__main__':
    framework()

