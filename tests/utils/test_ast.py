import unittest

from rtquery.utils.ast import Token, BinOp, Literal, StringLiteral
from rtquery.utils.consts import LITERAL, IS


class TokenTestCase(unittest.TestCase):
    def test_token(self):
        token = Token(LITERAL, 'Status')
        self.assertEqual(token, Token(LITERAL, 'Status'))

        self.assertEqual(repr(token), "Token(LITERAL, Status)")
        self.assertEqual(str(token), "Token(LITERAL, Status)")

    def test_literal(self):
        token = Token(LITERAL, 'Status')
        literal = Literal(token)
        self.assertEqual(repr(literal), "<Literal: Status>")
        self.assertEqual(str(literal), "<Literal: Status>")

    def test_stringliteral(self):
        token = Token(LITERAL, 'Status')
        literal = StringLiteral(token)
        self.assertEqual(repr(literal), "<StringLiteral: \"Status\">")
        self.assertEqual(str(literal), "<StringLiteral: \"Status\">")

    def test_binop(self):
        literal = Literal(Token(Literal, 'Status'))
        op = Token(IS, IS)
        string_literal = StringLiteral(Token(StringLiteral, "new"))
        binop = BinOp(left=literal, op=op, right=string_literal)

        self.assertEqual(
            repr(binop),
            '<BinOp (<Literal: Status>, Token(=, =), <StringLiteral: "new">)>'
        )
        self.assertEqual(
            str(binop),
            '<BinOp (<Literal: Status>, Token(=, =), <StringLiteral: "new">)>'
        )
