import binascii
import sys

from zope.interface import implements

from Products.statusmessages import STATUSMESSAGEKEY
from Products.statusmessages.message import decode
from Products.statusmessages.message import Message
from Products.statusmessages.interfaces import IStatusMessage

HAS_GTS = True
try:
    from Products.PageTemplates.GlobalTranslationService import \
        getGlobalTranslationService
except ImportError:
    HAS_GTS = False

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
        if HAS_GTS:
            gts = getGlobalTranslationService()
            parents = getattr(self.context, 'PARENTS', None)
            aq_context = parents is not None and parents[0] or None
            text = gts.translate(None, text, context=aq_context)

        value = _encodeCookieValue(text, type, old=self.context.cookies.get(STATUSMESSAGEKEY))
        self.context.cookies[STATUSMESSAGEKEY] = value
        self.context.RESPONSE.setCookie(STATUSMESSAGEKEY, value, path='/')

    def showStatusMessages(self):
        """Removes all status messages and returns them for display.
        """
        value = self.context.cookies.get(STATUSMESSAGEKEY)
        if value is None:
            return []
        value = _decodeCookieValue(value)
        # clear the existing cookie entries
        self.context.cookies[STATUSMESSAGEKEY] = None
        self.context.RESPONSE.expireCookie(STATUSMESSAGEKEY, path='/')
        return value


def _encodeCookieValue(text, type, old=None):
    """Encodes text and type to a list of Messages. If there is already some old
       existing list, add the new Message at the end but don't add duplicate
       messages.
    """
    results = []
    message = Message(text, type=type)

    if old is not None:
        results = _decodeCookieValue(old)
    if not message in results:
        results.append(message)

    messages = ''.join([r.encode() for r in results])
    return binascii.b2a_base64(messages).rstrip()

def _decodeCookieValue(string):
    """Decode a cookie value to a list of Messages.
    """
    results = []
    # Return nothing if the cookie is marked as deleted
    if string == 'deleted':
        return results
    # Try to decode the cookie value
    try:
        value = binascii.a2b_base64(string)
        while len(value) > 1: # at least 2 bytes of data
            message, value = decode(value)
            if message is not None:
                results.append(message)
    except (binascii.Error, UnicodeEncodeError):
        logger.log(logging.ERROR, '%s \n%s',
                   'Unexpected value in statusmessages cookie',
                   sys.exc_value
                   )
        return []

    return results
