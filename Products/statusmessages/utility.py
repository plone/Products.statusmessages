from zope.interface import implements

from Products.statusmessages.message import Message
from Products.statusmessages.interfaces import IStatusMessageUtility

global_messages = {}

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

        if global_messages.has_key(bid):
            global_messages[bid].append(message)
        else:
            global_messages[bid] = [message]

    def getStatusMessages(self, context):
        """Returns all status messages.
        """
        bim = context.browser_id_manager
        if bim.hasBrowserId():
            bid = bim.getBrowserId()
            return global_messages.get(bid, [])
        return []

    def clearStatusMessages(self, context):
        """Removes all status messages.
        """
        bim = context.browser_id_manager
        if bim.hasBrowserId():
            bid = bim.getBrowserId()
            if global_messages.has_key(bid):
                global_messages[bid] = []

    def showStatusMessages(self, context):
        """Removes all status messages and returns them for display.
        """
        messages = self.getStatusMessages(context)
        if messages is not []:
            self.clearStatusMessages(context)
        return messages

utility = StatusMessageUtility()
