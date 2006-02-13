from zope.interface import implements

from Products.statusmessages.interfaces import IMessage

class Message:
    """A single status message.

    Let's make sure that this implementation actually fulfills the
    'IMessage' API.

      >>> from zope.interface.verify import verifyClass
      >>> verifyClass(IMessage, Message)
      True
    
      >>> status = Message(u'this is a test', type=u'info')
      >>> status.message
      u'this is a test'

      >>> status.type
      u'info'

    It is quite common to use MessageID's as status messages:

      >>> from zope.i18nmessageid import MessageIDFactory, MessageID
      >>> msg_factory = MessageIDFactory('test')

      >>> msg = msg_factory(u'test_message', default=u'Default text')

      >>> status = Message(msg, type=u'warn')
      >>> status.type
      u'warn'

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

