from zope.interface import implements

from Products.statusmessages.interfaces import IStatusMessage
from Products.statusmessages.interfaces import IStatusMessageUtility

STATUS_KEY = 'status_messages'

class StatusMessage:
    """A single status message.

    Let's make sure that this implementation actually fulfills the
    'IStatusMessage' API.

      >>> from Products.statusmessages.interfaces import IStatusMessage
      >>> from Products.statusmessages.utility import StatusMessage

      >>> from zope.interface.verify import verifyClass
      >>> verifyClass(IStatusMessage, StatusMessage)
      True
    
      >>> status = StatusMessage(u'this is a test', type='info')
      >>> status.message
      u'this is a test'

      >>> status.type
      'info'

    It is quite common to use MessageID's as status messages:

      >>> from zope.i18nmessageid import MessageIDFactory, MessageID
      >>> msg_factory = MessageIDFactory('test')

      >>> msg = msg_factory(u'test_message', default=u'Default text')

      >>> status = StatusMessage(msg, type='warn')
      >>> status.type
      'warn'

      >>> type(status.message) is MessageID
      True

      >>> status.message.default
      u'Default text'

      >>> status.message.domain
      'test'

    """
    implements(IStatusMessage)

    def __init__(self, message, type=''):
        self.message = message
        self.type = type


class StatusMessageUtility(object):
    """Utility for handling status messages.
    
    Let's make sure that this implementation actually fulfills the
    'IStatusMessageUtility' API.

      >>> from Products.statusmessages.interfaces import IStatusMessageUtility
      >>> from Products.statusmessages.utility import StatusMessageUtility

      >>> from zope.interface.verify import verifyClass
      >>> verifyClass(IStatusMessageUtility, StatusMessageUtility)
      True

    """
    implements(IStatusMessageUtility)

    def addStatusMessage(self, env, text, type=''):
        """Add a status message.
        """
        message = StatusMessage(text, type)

        if env.has_key(STATUS_KEY):
            env[STATUS_KEY].append(message)
        else:
            env.set(STATUS_KEY, [message])

    def getStatusMessages(self, env):
        """Returns all status messages.
        """
        return env.get(STATUS_KEY)

    def clearStatusMessages(self, env):
        """Removes all status messages.
        """
        env.set(STATUS_KEY, [])

    def showStatusMessages(self, env):
        """Removes all status messages and returns them for display.
        """
        messages = self.getStatusMessages(env)
        self.clearStatusMessages(env)
        return messages

utility = StatusMessageUtility()
