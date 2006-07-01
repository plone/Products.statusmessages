import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase

from zope.app.tests import placelesssetup

from Products.Five import zcml
from Products.statusmessages.interfaces import IStatusMessage
from Products.statusmessages.statusmessage import SessionStatusMessage, STATUS_KEY
import Products.statusmessages, Products.statusmessages.tests

ZopeTestCase.utils.setupCoreSessions()

class TestStatusMessageSessionAdapter(ZopeTestCase.ZopeTestCase):

    def afterSetUp(self):
        placelesssetup.setUp()
        zcml.load_config('meta.zcml', Products.Five)
        zcml.load_config('configure.zcml', Products.statusmessages.tests)
        zcml.load_config('configure.zcml', Products.statusmessages)
        # Put SESSION object into REQUEST
        request = self.app.REQUEST
        sdm = self.app.session_data_manager
        request.set('SESSION', sdm.getSessionData())
        self.session = request.SESSION

    def testAdapter(self):
        status = IStatusMessage(self.app.REQUEST)
        
        status.addStatusMessage('test', 'info')
        self.failUnless(self.session[STATUS_KEY]==status.getStatusMessages())

        status.addStatusMessage('test2', 'warn')
        messages = status.showStatusMessages()
        self.failUnless(len(messages)==2)
        self.failUnless(len(status.getStatusMessages())==0)
        
        status.addStatusMessage('test', 'info')
        self.failUnless(self.session[STATUS_KEY]==status.getStatusMessages())
        status.clearStatusMessages()
        self.failUnless(len(status.getStatusMessages())==0)

    def beforeTearDown(self):
        placelesssetup.tearDown()


class TestStatusMessageRequestAdapter(ZopeTestCase.ZopeTestCase):

    def afterSetUp(self):
        placelesssetup.setUp()
        zcml.load_config('meta.zcml', Products.Five)
        zcml.load_config('configure.zcml', Products.statusmessages.tests)
        zcml.load_config('configure-request.zcml', Products.statusmessages.tests)

    def testAdapter(self):
        request = self.app.REQUEST
        status = IStatusMessage(request)
        
        status.addStatusMessage('test', 'info')
        self.failUnless(request[STATUS_KEY]==status.getStatusMessages())

        status.addStatusMessage('test2', 'warn')
        messages = status.showStatusMessages()
        self.failUnless(len(messages)==2)
        self.failUnless(len(status.getStatusMessages())==0)
        
        status.addStatusMessage('test', 'info')
        self.failUnless(request[STATUS_KEY]==status.getStatusMessages())
        status.clearStatusMessages()
        self.failUnless(len(status.getStatusMessages())==0)

    def beforeTearDown(self):
        placelesssetup.tearDown()

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestStatusMessageSessionAdapter))
    suite.addTest(makeSuite(TestStatusMessageRequestAdapter))
    return suite

if __name__ == '__main__':
    framework()

