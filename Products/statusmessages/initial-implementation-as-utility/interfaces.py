from zope.interface import Interface, Attribute

class IStatusMessage(Interface):
    """A single status message.
    """

    message = Attribute('The text of this message. Usally a Message object.')

    type = Attribute('The type of this message.')


class IStatusMessageUtility(Interface):
    """A utility for handling status messages."""

    def addStatusMessage(env, text, type=''):
        """Add a status message."""

    def getStatusMessages(env):
        """Returns all status messages.
        """

    def clearStatusMessages(env):
        """Removes all status messages."""

    def showStatusMessages(env):
        """Removes all status messages and returns them for display.
        """

