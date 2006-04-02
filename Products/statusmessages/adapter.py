from base64 import encodestring, decodestring
from pickle import dumps, loads
from zope.interface import implements

from Products.statusmessages import STATUSMESSAGEKEY
from Products.statusmessages.message import Message
from Products.statusmessages.interfaces import IStatusMessage

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
        self.cookies = self.context.RESPONSE.cookies

    def addStatusMessage(self, text, type=''):
        """Add a status message.
        """
        value = _encodeCookieValue(text, type,
                                   old=self.cookies.get(STATUSMESSAGEKEY))
        self.context.RESPONSE.setCookie(STATUSMESSAGEKEY, value)

    def showStatusMessages(self):
        """Removes all status messages and returns them for display.
        """
        value = self.cookies.get(STATUSMESSAGEKEY)
        if value is None:
            return []
        value = value.copy()
        # clear the existing cookie entries
        self.context.RESPONSE.setCookie(STATUSMESSAGEKEY, None)
        return _decodeCookieValue(value)

def _encodeCookieValue(text, type, old=None):
    """Encodes text and type to a list of Messages. If there is already some old
       existing list, add the new Message at the end.
    """
    results = []
    message = Message(text, type=type)

    if old is not None:
        results = _decodeCookieValue(old)
    results.append(message)
    return encodestring(dumps(results))

def _decodeCookieValue(string):
    """Decode a cookie value to a list of Messages.
       The value has to be a base64 encoded pickle of a list of Messages. If it
       contains anything else, it will be ignored for security reasons.
    """
    results = []
    try:
        values = loads(decodestring(string['value']))
    except: # If there's anything unexpected in the string ignore it
        return []
    if type(values) is list: # simple security check
        for value in values:
            if isinstance(value, Message): # and another simple check
                results.append(value)
    return results

