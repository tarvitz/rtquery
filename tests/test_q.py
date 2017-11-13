import sys
import unittest
from rtquery import Q
from copy import deepcopy
from types import GeneratorType


class TestQueryResolve(unittest.TestCase):
    def test_q_simple(self):
        if sys.version_info[:2] >= (3, 6):
            #: works in python3.4-3.5 too, but order is unpredictable
            #: to test it
            query = Q(Status='backlog', Subject__contains='[topic]',
                      Owner='Nobody')
            #: kwargs order saves according to PEP 468
            self.assertEqual(
                query.resolve(),
                "(Status = 'backlog' AND Subject LIKE '[topic]' "
                "AND Owner = 'Nobody')"
            )
        else:
            #: reverse order for older python versions so there's no good idea
            #: to test properly
            query = (
                Q(Status='backlog') & Q(Subject__contains='[topic]')
            ) & Q(Owner='Nobody')
            self.assertEqual(
                query.resolve(),
                "(Status = 'backlog' AND Subject LIKE '[topic]' "
                "AND Owner = 'Nobody')"
            )

    def test_q_nested(self):
        qset = (
            Q(Status="backlog")
            & Q(Id__gt=300000)
            | Q(Status="new")
            & Q(Owner="User")
        )
        self.assertEqual(
            qset.resolve(),
            "((Status = 'backlog' AND Id > 300000) OR "
            "(Status = 'new' AND Owner = 'User'))"
        )

    def test_q_negative(self):
        qset = ~Q(Status="backlog") | ~Q(Owner="Nobody")
        query = qset.resolve()
        self.assertEqual(query, "((Status != 'backlog') OR (Owner != 'Nobody'))")

    def test_q_complex(self):
        qset = (
            Q(Status='new') & Q(Owner='Nobody') & Q(Owner="User")
        ) | ~Q(Subject__contains='[topic]') & Q(Id__lt=3) & Q(Id__gt=1)
        self.assertEqual(
            qset.resolve(),
            "((Status = 'new' AND Owner = 'Nobody' AND Owner = 'User') OR "
            "((Subject NOT LIKE '[topic]') AND Id < 3 AND Id > 1))"
        )


class TestQInternals(unittest.TestCase):
    def test_combine(self):
        q = Q(blank=True)
        with self.assertRaises(TypeError) as err:
            q._combine(other=['wrong data chunk'], connector=Q.AND)

    def test_node_is_blank(self):
        self.assertFalse(Q())

    def test_node_add__duplicate(self):
        q = Q(blank=True)
        q.add(('blank', True), connector_type=Q.AND)
        self.assertEqual(len(q.children), 1)

    def test_node_add__squash(self):
        q = Q(blank=True)
        q.add(('blank', False), connector_type=Q.AND, squash=False)
        self.assertEqual(len(q.children), 2)

    def test_node_add__use_new_instance(self):
        source = Q(field=10)
        q = (
            Q(blank=True) | Q(blank=False)
        ).add(source, connector_type=Q.AND)
        self.assertEqual(len(q.children), 1)

    def test_node_deepcopy(self):
        q = Q(blank=True)
        new_q = deepcopy(q)
        self.assertEqual(q.children, new_q.children)

    def test_node_iter(self):
        q = Q(blank=True, field=10, query='blank')
        self.assertIsInstance(q.__iter__(), GeneratorType)
        entries = [x for x in q.__iter__()]

        self.assertEqual(len(entries), 3)
        self.assertIn(('blank', True), entries)
        self.assertIn(('field', 10), entries)
        self.assertIn(('query', 'blank'), entries)

    def test_node_contains(self):
        qset = Q(blank=True, empty=False)
        self.assertIn(Q(blank=True).children[0], qset)

    def test_node_str(self):
        q = Q(blank=True)
        self.assertEqual(str(q), "(AND: ('blank', True))")

        q = ~Q(blank=True)
        self.assertEqual(str(q), "(NOT (AND: ('blank', True)))")

    def test_node_repr(self):
        q = Q(blank=True)
        self.assertEqual(repr(q), "<Q: (AND: ('blank', True))>")
