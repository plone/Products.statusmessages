====================
About statusmessages
====================

statusmessages provides an easy way of handling internationalized status
messages managed via a global utility. It requires Zope >= 2.8.

It is quite common to write status messages which should be shown to the user
after some action. These messages of course should be internationalized. As
these messages normally are definied in Python code, the common way to i18n-ize
these in Zope is to use Zope3 MessageID's. MessageID's are complex objects
consisting of a translation domain and a default unicode text and might have an
additional mapping dict and a distinct id.

The usual way to provide status messages in CMF/Plone has been to add a
"?portal_status_messages=some%20text" to the URL. While this has some usability
problems it also isn't possible to i18n-ize these in the common way, as the URL
is currently limited to the ASCII charset, but an encoding providing support for
the full unicode range is required.

The solution provided by this tool is to use a session like approach. But as
sessions tend to be quite ressource intense, a simpler implementation has been
choosen. The two main differences to full sessions are, that status messages
don't need to be persisted and they live only for the duration of one
request/reponse pair.

In contrast to sessions this utility therfore does not implement any aging
capabilities but deletes all status messages once there are shown. For user
identification the implementation currently relies on the BrowserIdManager from
Zope2's sessions module and in effect does not run natively on Zope3.

Status messages are kept in a in-memory module-scope dict with a wrapper around
it making it thread-safe. In a ZEO environment this means, that you might have
to use an intelligent load-balancer to keep users talking to the same ZEO
instance all the time or you might get some funny effects where status messages
are not shown at first, but might pop-up at a later time.

- History in HISTORY.txt

- License terms in LICENSE.txt

Read more at http://plone.org/products/statusmessages

