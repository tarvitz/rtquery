import unittest

from rtquery.utils.lexer import Lexer
from rtquery.utils.parser import FilterParser, ParserError
from rtquery.utils.consts import LITERAL, STRING_LITERAL, IS, INTEGER, MINUS
from rtquery.utils.ast import BinOp, UnaryOp, Num, Token


class FilterParserTestCase(unittest.TestCase):
    def test_simple_binary_operations(self):
        node = FilterParser(lexer=Lexer("Status='new'")).parse()
        self.assertIsInstance(node, BinOp)
        self.assertEqual(node.left.token, Token(LITERAL, "Status"))
        self.assertEqual(node.right.token, Token(STRING_LITERAL, "new"))
        self.assertEqual(node.op, Token(IS, "="))

        node = FilterParser(lexer=Lexer("Status=new")).parse()
        self.assertIsInstance(node, BinOp)
        self.assertEqual(node.right.token, Token(LITERAL, "new"))

    def test_unary_operations(self):
        node = FilterParser(lexer=Lexer("Age=-10")).parse()
        self.assertIsInstance(node, BinOp)
        self.assertIsInstance(node.right, UnaryOp)
        self.assertIsInstance(node.right.expr, Num)
        self.assertEqual(node.right.expr.token, Token(INTEGER, 10))
        self.assertEqual(node.right.token, Token(MINUS, '-'))

    def test_parser_error(self):
        with self.assertRaises(ParserError) as err:
            FilterParser(Lexer(">20=50")).parse()
        self.assertEqual(
            err.exception.args,
            ("Statement should start with Literal or StringLiteral, "
             "'Token(>, >)' given",)
        )

        with self.assertRaises(ParserError):
            FilterParser(Lexer("10 ~ text")).parse()

        with self.assertRaises(ParserError):
            FilterParser(Lexer("& ~ text")).parse()

    def test_parser_error_in_composite(self):
        with self.assertRaises(ParserError) as err:
            FilterParser(Lexer("Status=&")).parse()
        self.assertEqual(
            err.exception.args,
            ("Wrong statement right part: 'Token(&, &)'",)
        )

    def test_parser_error_in_statement(self):
        with self.assertRaises(ParserError) as err:
            FilterParser(Lexer("Status&1")).parse()
        self.assertEqual(
            err.exception.args,
            ("Wrong operation '&' for statement given",)
        )
