import unittest

from rtquery.utils.parser import FilterParser
from rtquery.utils.lexer import Lexer
from rtquery.utils.visitors import NodeVisitor, VisitError
from rtquery.utils.ast import BinOp

from rtquery import Q


class NodeVisitorTestCase(unittest.TestCase):
    def test_node_visitor(self):
        text = "Status = 'new'"
        ast = FilterParser(Lexer(text)).parse()
        self.assertIsInstance(ast, BinOp)

        base_visitor = NodeVisitor()
        with self.assertRaises(VisitError) as err:
            self.assertIsInstance(base_visitor.visit(ast), Q)
        self.assertEqual(
            err.exception.args,
            ("No visit_%s method" % type(ast).__name__.lower(),)
        )
