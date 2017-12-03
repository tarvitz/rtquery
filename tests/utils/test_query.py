import unittest
from unittest import mock

from rtquery import Q
from rtquery.utils import (
    query, ReadError, ERROR_PARSER, ERROR_VISITOR, ERROR_INTERPRETER,
    ERROR_LEXER
)
from rtquery.utils import visitors, operations


class FilterParserTestCase(unittest.TestCase):
    def test_query_is(self):
        qset = query("Status = 'new'")
        self.assertIsInstance(qset, Q)
        self.assertEqual(qset.resolve(), "(Status = 'new')")

    def test_query_is_not(self):
        qset = query("Status != 'new'")
        self.assertIsInstance(qset, Q)
        self.assertEqual(qset.resolve(), "(Status != 'new')")

    def test_query_gt(self):
        qset = query("Age > 10")
        self.assertIsInstance(qset, Q)
        self.assertEqual(qset.resolve(), "(Age > 10)")

    def test_query_lt(self):
        qset = query("DaysPassed < 1337")
        self.assertIsInstance(qset, Q)
        self.assertEqual(qset.resolve(), "(DaysPassed < 1337)")

    def test_query_matches(self):
        qset = query("Status ~ 'I like hot dogs'")
        self.assertIsInstance(qset, Q)
        self.assertEqual(qset.resolve(), "(Status LIKE 'I like hot dogs')")

    def test_query_does_not_match(self):
        qset = query("Status !~ 'I like hot dogs'")
        self.assertIsInstance(qset, Q)
        self.assertEqual(qset.resolve(), "(Status NOT LIKE 'I like hot dogs')")

    def test_query_or_simple(self):
        qset = query("(Status = resolve) | (Status = open)")
        self.assertIsInstance(qset, Q)
        self.assertEqual(
            qset.resolve(), "((Status = 'resolve') OR (Status = 'open'))"
        )

    def test_query_or_complex(self):
        qset = query(
            "(Status = resolve & Age = 17) | (Status = open & Age = 13)"
        )
        self.assertIsInstance(qset, Q)

        self.assertEqual(
            qset.resolve(),
            "(((Status = 'resolve') AND (Age = 17)) OR "
            "((Status = 'open') AND (Age = 13)))"
        )

    def test_query_and_simple(self):
        qset = query("Status = resolve & Owner = user")
        self.assertIsInstance(qset, Q)

        self.assertEqual(
            qset.resolve(),
            "((Status = 'resolve') AND (Owner = 'user'))"
        )

    def test_query_and_complex(self):
        qset = query("(Status = resolve & Owner = user) | Ticket > 1000")
        self.assertIsInstance(qset, Q)
        self.assertEqual(
            qset.resolve(),
            "(((Status = 'resolve') AND (Owner = 'user')) OR (Ticket > 1000))"
        )

    def test_query_read_error(self):
        with self.assertRaises(ReadError) as err:
            query(">10")
        self.assertEqual(err.exception.err_type, ERROR_PARSER)

        with self.assertRaises(ReadError) as err:
            query("%")
        self.assertEqual(err.exception.err_type, ERROR_LEXER)

        with mock.patch(
                    'rtquery.utils.interpreter.'
                    'FilterQueryInterpreter.visit_literal') as m:
            m.side_effect = visitors.VisitError("blank")
            with self.assertRaises(ReadError) as err:
                query("Status=new")
        self.assertEqual(err.exception.err_type, ERROR_VISITOR)

        with mock.patch.object(operations, 'BINARY_OPERATIONS', {}):
            with self.assertRaises(ReadError) as err:
                query("Status=new")
        self.assertEqual(err.exception.err_type, ERROR_INTERPRETER)

    def test_query_type_error(self):
        with self.assertRaises(TypeError) as err:
            query("Status=-open")
        self.assertEqual(err.exception.args,
                         ("bad operand type for unary -: 'str'",))
