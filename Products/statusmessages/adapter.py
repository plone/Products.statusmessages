from base64 import encodestring, decodestring
from pickle import dumps, loads
import sys

from zope.interface import implements

from Products.statusmessages import STATUSMESSAGEKEY
from Products.statusmessages.message import Message
from Products.statusmessages.interfaces import IStatusMessage

import logging
logger = logging.getLogger('statusmessages')

class StatusMessage(object):
    """Adapter for the BrowserRequest to handle status messages.
    
    Let's make sure that this implementation actually fulfills the
    'IStatusMessage' API.

      >>> from zope.interface.verify import verifyClass
      >>> verifyClass(IStatusMessage, StatusMessage)
      True
    """
    implements(IStatusMessage)

    def __init__(self, context):
        self.context = context # the context must be the request

    def addStatusMessage(self, text, type=''):
        """Add a status message.
        """
        value = _encodeCookieValue(text, type, old=self.context.cookies.get(STATUSMESSAGEKEY))
        self.context.RESPONSE.setCookie(STATUSMESSAGEKEY, value)

    def showStatusMessages(self):
        """Removes all status messages and returns them for display.
        """
        value = self.context.cookies.get(STATUSMESSAGEKEY)
        if value is None:
            return []
        value = _decodeCookieValue(value)
        # clear the existing cookie entries
        self.context.RESPONSE.expireCookie(STATUSMESSAGEKEY)
        return value

def _encodeCookieValue(text, type, old=None):
    """Encodes text and type to a list of Messages. If there is already some old
       existing list, add the new Message at the end.
    """
    results = []
    message = Message(text, type=type)

    if old is not None:
        results = _decodeCookieValue(old)
    results.append(message)
    # we have to remove any newlines or the cookie value will be invalid
    return encodestring(dumps(results)).replace('\n','')

def _decodeCookieValue(string):
    """Decode a cookie value to a list of Messages.
       The value has to be a base64 encoded pickle of a list of Messages. If it
       contains anything else, it will be ignored for security reasons.
    """
    results = []
    # Return nothing if the cookie is marked as deleted
    if string == 'deleted':
        return results
    # Try to decode the cookie value
    try:
        values = loads(decodestring(string))
    except: # If there's anything unexpected in the string ignore it
        logger.log(logging.ERROR, '%s \n%s',
                   'Unexpected value in statusmessages cookie',
                   sys.exc_value
                   )
        return []
    if type(values) is list: # simple security check
        for value in values:
            if isinstance(value, Message): # and another simple check
                results.append(value)
    return results
