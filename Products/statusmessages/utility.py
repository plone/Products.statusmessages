from zope.interface import implements

from Products.statusmessages.message import Message
from Products.statusmessages.interfaces import IStatusMessageUtility

_MESSAGES = {}

import threading

class ThreadSafeDict:
    """This is a thread-safe dict implementation.
    """
    lock = threading.RLock()

    def has_key(self, k):
        self.lock.acquire()
        try:
            return _MESSAGES.has_key(k)
        finally:
            self.lock.release()

    def get(self, k):
        self.lock.acquire()
        try:
            return _MESSAGES.get(k)
        finally:
            self.lock.release()

    def set(self, k, v):
        self.lock.acquire()
        try:
            _MESSAGES[k] = v
        finally:
            self.lock.release()

_messages = ThreadSafeDict()

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

    def addStatusMessage(self, context, text, type=''):
        """Add a status message.
        """
        message = Message(text, type)

        bim = context.browser_id_manager
        # This creates a new browserid if none is available
        bid = bim.getBrowserId()

        if _messages.has_key(bid):
            msgs = _messages.get(bid)
            msgs.append(message)
            _messages.set(bid, msgs)
        else:
            _messages.set(bid, [message])

    def getStatusMessages(self, context):
        """Returns all status messages.
        """
        bim = context.browser_id_manager
        if bim.hasBrowserId():
            bid = bim.getBrowserId()
            if _messages.has_key(bid):
                return _messages.get(bid)
        return []

    def clearStatusMessages(self, context):
        """Removes all status messages.
        """
        bim = context.browser_id_manager
        if bim.hasBrowserId():
            bid = bim.getBrowserId()
            if _messages.has_key(bid):
                _messages.set(bid, [])

    def showStatusMessages(self, context):
        """Removes all status messages and returns them for display.
        """
        messages = self.getStatusMessages(context)
        if messages is not []:
            self.clearStatusMessages(context)
        return messages

utility = StatusMessageUtility()
