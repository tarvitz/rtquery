import unittest

from rtquery.utils.ast import Token
from rtquery.utils.consts import LITERAL


class TokenTestCase(unittest.TestCase):
    def test_token(self):
        token = Token(LITERAL, 'Status')
        self.assertEqual(token, Token(LITERAL, 'Status'))

        self.assertEqual(repr(token), "Token(LITERAL, Status)")
        self.assertEqual(str(token), "Token(LITERAL, Status)")
