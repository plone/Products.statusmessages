# -*- coding: UTF-8 -*-
import unittest

class TestEncoding(unittest.TestCase):

    def test_encoding_msg_with_type(self):
        """Test message encoding:
        """
        from Products.statusmessages.message import Message
        from Products.statusmessages.message import decode
        m = Message(u'späm', u'eggs')
        self.assertEqual(
            m.encode(),
            '\x00\xa4sp\xc3\xa4meggs'
        )
        self.assertEqual(decode(m.encode())[0], m)

    def test_encoding_msg_without_type(self):
        from Products.statusmessages.message import Message
        from Products.statusmessages.message import decode
        m = Message(u'späm')
        self.assertEqual(
            m,
            Message(u'späm'),
        )
        self.assertEqual(m.encode(), '\x00\xa0sp\xc3\xa4m')
        self.assertEqual(decode(m.encode())[0], m)

    def test_decoding(self):
        """Test message decoding:
        """
        from Products.statusmessages.message import Message
        from Products.statusmessages.message import decode

        # Craft a wrong value:
        m, rem = decode('\x01\x84spameggs')
        self.assertEqual(
            m.message,
            u'spameggs',
        )
        self.assertEqual(
          m.type,
          u'',
        )
        self.assertEqual(rem, '')

        # Craft another wrong value:
        m, rem = decode('\x00\x24spameggs')
        self.assertEqual(
            m.message,
            u's',
        )
        self.assertEqual(
          m.type,
          u'pame',
        )
        self.assertEqual(rem, 'ggs')

        # And another wrong value:
        m, rem = decode('\x00spameggs')
        self.assertEqual(
            m.message,
            u'pam',
        )
        self.assertEqual(
          m.type,
          u'eggs',
        )
        self.assertEqual(rem, '')

        # And yet another wrong value:
        m, rem = decode('')

        self.assertIs(m, None)
        self.assertEqual(rem , '')
