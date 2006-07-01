from zope.interface import implements

from Products.statusmessages.interfaces import IMessage
from Products.statusmessages.interfaces import IStatusMessage

STATUS_KEY = 'status_messages'

class Message:
    """A single status message.

    Let's make sure that this implementation actually fulfills the
    'IMessage' API.

      >>> from Products.statusmessages.interfaces import IMessage
      >>> from Products.statusmessages.statusmessage import Message

      >>> from zope.interface.verify import verifyClass
      >>> verifyClass(IMessage, Message)
      True
    
      >>> status = Message(u'this is a test', type='info')
      >>> status.message
      u'this is a test'

      >>> status.type
      'info'

    It is quite common to use MessageID's as status messages:

      >>> from zope.i18nmessageid import MessageIDFactory, MessageID
      >>> msg_factory = MessageIDFactory('test')

      >>> msg = msg_factory(u'test_message', default=u'Default text')

      >>> status = Message(msg, type='warn')
      >>> status.type
      'warn'

      >>> type(status.message) is MessageID
      True

      >>> status.message.default
      u'Default text'

      >>> status.message.domain
      'test'

    """
    implements(IMessage)

    def __init__(self, message, type=''):
        self.message = message
        self.type = type


class RequestStatusMessage(object):
    """Adapter for handling status messages in the request.
    
    Let's make sure that this implementation actually fulfills the
    'IStatusMessage' API.

      >>> from Products.statusmessages.interfaces import IStatusMessage
      >>> from Products.statusmessages.statusmessage import RequestStatusMessage

      >>> from zope.interface.verify import verifyClass
      >>> verifyClass(IStatusMessage, RequestStatusMessage)
      True

    """
    implements(IStatusMessage)
    
    def __init__(self, context):
        self.context = context

    def addStatusMessage(self, text, type=''):
        """Add a status message.
        """
        message = Message(text, type)
        
        if self.context.has_key(STATUS_KEY):
            self.context[STATUS_KEY].append(message)
        else:
            self.context.set(STATUS_KEY, [message])

    def getStatusMessages(self):
        """Returns all status messages.
        """
        return self.context.get(STATUS_KEY)

    def clearStatusMessages(self):
        """Removes all status messages.
        """
        self.context.set(STATUS_KEY, [])

    def showStatusMessages(self):
        """Removes all status messages and returns them for display.
        """
        messages = self.getStatusMessages()
        self.clearStatusMessages()
        return messages


class SessionStatusMessage(object):
    """Adapter for handling status messages in the session.
    
    Let's make sure that this implementation actually fulfills the
    'IStatusMessage' API.

      >>> from Products.statusmessages.interfaces import IStatusMessage
      >>> from Products.statusmessages.statusmessage import SessionStatusMessage

      >>> from zope.interface.verify import verifyClass
      >>> verifyClass(IStatusMessage, SessionStatusMessage)
      True

    """
    implements(IStatusMessage)
    
    def __init__(self, context):
        self.context = context

    def addStatusMessage(self, text, type=''):
        """Add a status message.
        """
        message = Message(text, type)
        
        if self.context.SESSION.has_key(STATUS_KEY):
            self.context.SESSION.get(STATUS_KEY).append(message)
        else:
            self.context.SESSION.set(STATUS_KEY, [message])

    def getStatusMessages(self):
        """Returns all status messages.
        """
        return self.context.SESSION.get(STATUS_KEY)

    def clearStatusMessages(self):
        """Removes all status messages.
        """
        self.context.SESSION.set(STATUS_KEY, [])

    def showStatusMessages(self):
        """Removes all status messages and returns them for display.
        """
        messages = self.getStatusMessages()
        self.clearStatusMessages()
        return messages

