import unittest
from unittest import mock

from rtquery.utils.interpreter import FilterQueryInterpreter, InterpreterError
from rtquery.utils.parser import FilterParser
from rtquery.utils.lexer import Lexer
from rtquery.utils import operations, consts

from rtquery import Q


class FilterParserTestCase(unittest.TestCase):
    def test_binary_expression(self):
        text = "Status = 'new'"
        qset = FilterQueryInterpreter(FilterParser(Lexer(text))).interpret()
        self.assertIsInstance(qset, Q)
        self.assertEqual(qset.resolve(), "(Status = 'new')")

    def test_unary_expression(self):
        text = "Age > -10"
        qset = FilterQueryInterpreter(FilterParser(Lexer(text))).interpret()
        self.assertIsInstance(qset, Q)
        self.assertEqual(qset.resolve(), "(Age > -10)")

        text = "Age > --10"
        qset = FilterQueryInterpreter(FilterParser(Lexer(text))).interpret()
        self.assertIsInstance(qset, Q)
        self.assertEqual(qset.resolve(), "(Age > 10)")

    def test_unary_expression_literal(self):
        text = "Status > -open"
        with self.assertRaises(TypeError) as err:
            qset = FilterQueryInterpreter(
                FilterParser(Lexer(text))
            ).interpret()
        self.assertEqual(
            err.exception.args, ("bad operand type for unary -: 'str'",)
        )

    def test_wrong_binary_operation(self):
        text = "Status = 'new'"

        with mock.patch.object(operations, 'BINARY_OPERATIONS', {}):
            with self.assertRaises(InterpreterError) as err:
                FilterQueryInterpreter(FilterParser(Lexer(text))).interpret()

        self.assertEqual(
            err.exception.args,
            ("Operation: '%s' is not supported" % consts.IS, )
        )

    def test_wrong_unary_operation(self):
        text = "Age > -10"

        with mock.patch.object(operations, 'UNARY_OPERATIONS', {}):
            with self.assertRaises(InterpreterError) as err:
                FilterQueryInterpreter(FilterParser(Lexer(text))).interpret()

        self.assertEqual(
            err.exception.args,
            ("Operation: '%s' is not supported" % consts.MINUS, )
        )
