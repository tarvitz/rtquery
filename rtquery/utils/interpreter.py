from . import visitors, operations

OPERATION_IS_NOT_SUPPORTED = "Operation: '%s' is not supported"
BAD_OPERAND_TYPE = "bad operand type for unary %s: '%r'"


class InterpreterError(Exception):
    """
    Errors caught while interpreting process
    """


class FilterQueryInterpreter(visitors.NodeVisitor):
    """
    Converts AST with nodes to :py:class:`rtquery.Q` tree for further search

    :param rtquery.utils.parser.FilterParser parser:
    """

    def __init__(self, parser):
        self.parser = parser

    def visit_binop(self, node):
        op = node.op
        operation = operations.BINARY_OPERATIONS.get(node.op.type, None)
        if operation is None:
            raise InterpreterError(OPERATION_IS_NOT_SUPPORTED % op.type)
        return operation(self.visit(node.left), self.visit(node.right))

    def visit_unaryop(self, node):
        op = node.op
        operation = operations.UNARY_OPERATIONS.get(op.type, None)
        if operation is None:
            raise InterpreterError(OPERATION_IS_NOT_SUPPORTED % op.type)
        return operation(self.visit(node.expr))

    @staticmethod
    def visit_num(node):
        return node.value

    @staticmethod
    def visit_literal(node):
        return node.value

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)
