"""
    Status messages adapter tests.
"""

import unittest

from Products.statusmessages.message import Message
from Products.statusmessages.adapter import StatusMessage

def test_directives():
    """
    Test status messages

    First some boilerplate.

      >>> from zope.component.testing import setUp
      >>> setUp()

      >>> import Products.Five
      >>> import Products.statusmessages
      >>> import Products.statusmessages.tests

      >>> from Products.Five import zcml
      >>> zcml.load_config('meta.zcml', Products.Five)
      >>> zcml.load_config('configure.zcml', Products.statusmessages)
      >>> zcml.load_config('configure.zcml', Products.statusmessages.tests)

    Now lets make sure we can actually adapt the request.

      >>> from Products.statusmessages.interfaces import IStatusMessage
      >>> status = IStatusMessage(self.app.REQUEST)
      >>> IStatusMessage.providedBy(status)
      True

    The dummy request we have is a bit limited, so we need a simple method
    to fake a real request/response for the cookie handling. Basically it
    puts all entries from RESPONSE.cookies into REQUEST.cookies but shifts
    the real values into the right place as browsers would do it.
      
      >>> def fakePublish(request):
      ...     cookies = request.RESPONSE.cookies.copy()
      ...     new_cookies = {}
      ...     for key in cookies.keys():
      ...         new_cookies[key] = cookies[key]['value']
      ...     request.cookies = new_cookies
      ...     request.RESPONSE.cookies = {}

      >>> request = self.app.REQUEST
      >>> status = IStatusMessage(request)

    Make sure there's no stored message.

      >>> len(status.showStatusMessages())
      0

    Add one message
      
      >>> status.addStatusMessage(u'test', type=u'info')

    Now check the results

      >>> fakePublish(request)
      >>> messages = status.showStatusMessages()

      >>> len(messages)
      1

      >>> messages[0].message
      u'test'

      >>> messages[0].type
      u'info'

    Make sure messages are removed

      >>> len(status.showStatusMessages())
      0

    Add two messages

      >>> status.addStatusMessage(u'test', type=u'info')
      >>> fakePublish(request)
      >>> status.addStatusMessage(u'test1', u'warn')
      
    And check the results again

      >>> fakePublish(request)
      >>> messages = status.showStatusMessages()

      >>> len(messages)
      2

      >>> test = messages[1]

      >>> test.message
      u'test1'

      >>> test.type
      u'warn'

    Finally make sure messages are removed again

      >>> len(status.showStatusMessages())
      0

    Test incredibly long messages:

      >>> status.addStatusMessage(u'm' * 0x400, type=u't' * 0x20)

      And check the results again

      >>> fakePublish(request)
      >>> messages = status.showStatusMessages()
      >>> len(messages)
      1

      >>> test = messages[0]

      >>> test.message == u'm' * 0x3FF
      True

      Messages are stored as base64-ed cookie values, so we must make sure we
      create proper header values; all ascii characters, and no newlines:

        >>> status.addStatusMessage(u'test' * 40, type=u'info')
        >>> cookies = [c['value'] for c in request.RESPONSE.cookies.values()]
        >>> cookies = ''.join(cookies)
        >>> cookies == unicode(cookies).encode('ASCII')
        True
        >>> '\\n' in cookies
        False

      >>> test.type == u't' * 0x1F
      True

      >>> from zope.component.testing import tearDown
      >>> tearDown()
    """

def test_suite():
    from Testing.ZopeTestCase import ZopeDocTestSuite
    return ZopeDocTestSuite()

if __name__ == '__main__':
    unittest.main(defaultTest="test_suite")
