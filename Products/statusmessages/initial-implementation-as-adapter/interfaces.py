from zope.interface import Interface, Attribute

class IMessage(Interface):
    """A single status message.
    """

    message = Attribute('The text of this message. Usally a Message object.')

    type = Attribute('The type of this message.')


class IStatusMessage(Interface):
    """A single status message.
    """

    def addStatusMessage(text, type=''):
        """Add a status message."""

    def getStatusMessages():
        """Returns all status messages.
        """

    def clearStatusMessages():
        """Removes all status messages."""

    def showStatusMessages():
        """Removes all status messages and returns them for display.
        """

