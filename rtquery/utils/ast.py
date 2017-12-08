class Token(object):
    __slots__ = ['type', 'value']

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '%(class_name)s(%(type)s, %(value)s)' % {
            'class_name': self.__class__.__name__,
            'type': self.type,
            'value': self.value
        }

    def __eq__(self, other):
        return other.type == self.type and other.value == self.value


class AST(object):
    pass


class Literal(AST):
    """
    Literal structure, example:

    - Status
    - A_New_Field
    - etc

    :param rtquery.utils.ast.Token token: token to capture
    """
    __slots__ = ['token', 'value']

    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.value)

    def __str__(self):
        return repr(self)


class StringLiteral(Literal):
    """
    String Literal, Example:

    - "I like tomatoes"
    - "Simple-string"
    - "\n\n\n\nstring"
    - 'etc'
    """
    __slots__ = ['token', 'value']

    def __repr__(self):
        return '<%s: \"%s\">' % (self.__class__.__name__, self.value)

    def __str__(self):
        return repr(self)


class Num(AST):
    """
    Integer number structure:

    - 1
    - 2
    - 1337
    - 0
    """
    __slots__ = ['token', 'value']

    def __init__(self, token):
        self.token = token
        self.value = token.value


class BinOp(AST):
    """
    Binary Operation

    :param [Literal, StringLiteral] left: left operand
    :param Token op: operator token, Binary operations
    :param [Literal, StringLiteral, Num] right: right operand
    """
    __slots__ = ['left', 'token', 'right']

    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __repr__(self):
        return '<%s (%s, %s, %s)>' % (
            self.__class__.__name__,
            self.left, self.op, self.right
        )

    def __str__(self):
        return repr(self)


class UnaryOp(AST):
    """
    Unary operations node

    :param Token op: operator
    :param AST expr: expression
    """
    __slots__ = ['op', 'expr']

    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr
