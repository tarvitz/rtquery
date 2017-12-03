from functools import partial

from rtquery import Q
from . import consts


def op_is(left, right, negate=False):
    if negate:
        return ~Q(**{left: right})
    return Q(**{left: right})


def op_matches(left, right, negate=False):
    if negate:
        return ~Q(**{'%s__contains' % left: right})
    return Q(**{'%s__contains' % left: right})


def op_gt(left, right, negate=False):
    return Q(**{'%s__gt' % left: right})


def op_lt(left, right):
    return Q(**{'%s__lt' % left: right})


def op_or(left, right):
    return Q(left) | Q(right)


def op_and(left, right):
    return Q(left) & Q(right)


def op_unary_minus(right):
    return -right


op_is_not = partial(op_is, negate=True)
op_does_not_match = partial(op_matches, negate=True)

BINARY_OPERATIONS = {
    consts.IS: op_is,
    consts.IS_NOT: op_is_not,
    consts.MATCHES: op_matches,
    consts.MATCHES_NOT: op_does_not_match,
    consts.GREAT_THAN: op_gt,
    consts.LESS_THAN: op_lt,
    consts.AND: op_and,
    consts.OR: op_or
}
UNARY_OPERATIONS = {
    consts.MINUS: op_unary_minus,
}
