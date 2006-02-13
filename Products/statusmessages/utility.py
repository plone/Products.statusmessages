from zope.interface import implements

from Products.statusmessages.message import Message
from Products.statusmessages.interfaces import IStatusMessageUtility

_MESSAGES = {}

import threading

class ThreadSafeDict:
    """This is a thread-safe dict implementation.
    """
    lock = threading.RLock()

    def __getitem__(self, key):
        self.lock.acquire()
        try:
            return _MESSAGES.get(key)
        finally:
            self.lock.release()

    def __setitem__(self, key, value):
        self.lock.acquire()
        try:
            _MESSAGES[key] = value
        finally:
            self.lock.release()

    def __delitem__(self, key):
        self.lock.acquire()
        try:
            del(_MESSAGES[key])
        finally:
            self.lock.release()

    def has_key(self, key):
        self.lock.acquire()
        try:
            return _MESSAGES.has_key(key)
        finally:
            self.lock.release()

    def setdefault(self, key, value=None):
        self.lock.acquire()
        try:
            return _MESSAGES.setdefault(key, value)
        finally:
            self.lock.release()


_messages = ThreadSafeDict()

class StatusMessageUtility(object):
    """Utility for handling status messages.
    
    Let's make sure that this implementation actually fulfills the
    'IStatusMessageUtility' API.

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

        msgs = _messages.setdefault(bid, [])
        msgs.append(message)
        _messages[bid] = msgs

    def showStatusMessages(self, context):
        """Removes all status messages and returns them for display.
        """
        bim = context.browser_id_manager
        if bim.hasBrowserId():
            bid = bim.getBrowserId()
            if _messages.has_key(bid):
                msgs = _messages[bid]
                del(_messages[bid])
                return msgs
        return []

utility = StatusMessageUtility()
