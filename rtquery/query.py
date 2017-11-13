from typing import Tuple, Union
from . tree import Node

OPERATION_DEFAULT = '='
OPERATION_MAP = {
    'contains': 'LIKE',
    'equal': '=',
    'gt': '>',
    'lt': '<',
    '=': '='
}
NEGATIVE_CONVERSION_MAP = {
    '=': '!=',
    'contains': 'NOT LIKE',
    'equal': '!=',
    'gt': '<',
    'lt': '>',
}


class Q(Node):
    """
    Encapsulates filters as objects that can then be combined logically (using
    `&` and `|`). (taken from django)
    """
    OR = 'OR'
    AND = 'AND'
    default = AND

    def __init__(self, *args, **kwargs):
        super().__init__(children=list(args) + list(kwargs.items()))

    def _combine(self, other, connector):
        if not isinstance(other, Q):
            raise TypeError("`%s` requested, passed: `%r`" % (Q, other))

        obj = type(self)()
        obj.connector = connector
        obj.add(self, connector)
        obj.add(other, connector)
        return obj

    def __or__(self, other):
        return self._combine(other, self.OR)

    def __and__(self, other):
        return self._combine(other, self.AND)

    def __invert__(self):
        obj = type(self)()
        obj.add(self, self.AND)
        obj.negate()
        return obj

    def resolve(self) -> str:
        """
        Resolves :py:class:`rtquery.query.Q` object to string request

        :return: query request in string form
        """
        q = []
        for el in self.children:
            if isinstance(el, Q):
                q.append(el.resolve())
            else:
                field, operation, value = format_request(el, self.negated)
                q.append('%s %s %s' % (field, operation, value))
        return '(%s)' % (' %s ' % self.connector).join(q)


def format_request(element: Q, negated: bool) -> \
            Tuple[str, str, Union[str, int]]:
    """
    Processes element :py:class:`rtquery.query.Q` instance and returns back
    tuple with: ``field``, ``operation``, ``value``

    :param element:
    :param negated: if element has ``negated`` state
    :return: tuple of (field, operation, value)
    """
    raw_field, value = element
    field, *operation = raw_field.split('__')
    try:
        operation = operation.pop()
    except IndexError:
        operation = OPERATION_DEFAULT
    if negated:
        operation = NEGATIVE_CONVERSION_MAP[operation]
    else:
        operation = OPERATION_MAP[operation]

    if isinstance(value, str):
        value = '\'%s\'' % value
    return field, operation, value
