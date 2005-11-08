import os, sys
if __name__ == "__main__":
    execfile(os.path.join(sys.path[0], "framework.py"))

from Testing import ZopeTestCase
from Products.Sessions.tests.testSessionDataManager import TestBase

from zope.app import zapi
from zope.app.tests import ztapi, placelesssetup

from Products.Five import zcml
from Products.statusmessages.interfaces import IStatusMessageUtility
from Products.statusmessages.utility import utility, STATUS_KEY
import Products.statusmessages

class TestStatusMessageUtility(TestBase):

    def setUp(self):
        TestBase.setUp(self)
        placelesssetup.setUp()
        zcml.load_config('meta.zcml', Products.Five)
        zcml.load_config('configure.zcml', Products.statusmessages)

    def testUtilityLookup(self):
        util = zapi.getUtility(IStatusMessageUtility)
        self.failUnless(IStatusMessageUtility.providedBy(util))

    def testUtility(self):
        util = zapi.getUtility(IStatusMessageUtility)
        session = self.app.session_data_manager.getSessionData()
        
        util.addStatusMessage(session, 'test', 'info')
        self.failUnless(session[STATUS_KEY]==util.getStatusMessages(session))

        util.addStatusMessage(session, 'test2', 'warn')
        messages = util.showStatusMessages(session)
        self.failUnless(len(messages)==2)
        self.failUnless(len(util.getStatusMessages(session))==0)
        
        util.addStatusMessage(session, 'test', 'info')
        self.failUnless(session[STATUS_KEY]==util.getStatusMessages(session))
        util.clearStatusMessages(session)
        self.failUnless(len(util.getStatusMessages(session))==0)

    def tearDown(self):
        TestBase.tearDown(self)
        placelesssetup.tearDown()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestStatusMessageUtility))
    return suite

if __name__ == '__main__':
    framework()

