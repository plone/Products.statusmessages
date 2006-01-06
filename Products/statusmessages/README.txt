====================
About statusmessages
====================

statusmessages provides an easy way of handling status messages managed via a
global utility. It requires Zope >= 2.8.

It currently relies on the BrowserIdManager from Zope2's sessions module for
user identification and in effect does not run natively on Zope3.

Status messages are kept in a in-memory module-scope dict with a wrapper around
it making it thread-safe. In a ZEO environment this means, that you might have
to use an intelligent load-balancer to keep users talking to the same ZEO
instance all the time or you might get some funny effects where status messages
are not shown at first but might pop-up at a later time.

In contrast to sessions this utility does not implement any aging capabilities
but deletes all status messages once there are shown.

- History in HISTORY.txt

- License terms in LICENSE.txt

Read more at http://plone.org/products/statusmessages

