class VisitError(Exception):
    """
    If there was a visit exception during node operating
    """


class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__.lower()
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise VisitError(
            "No visit_{} method".format(type(node).__name__.lower())
        )
