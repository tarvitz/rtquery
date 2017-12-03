from . consts import (
    LITERAL, STRING_LITERAL, LPAREN, RPAREN, INTEGER, MINUS,
    LOW_PRIORITY_OPS, HIGH_PRIORITY_OPS
)

from . ast import Literal, BinOp, Num, UnaryOp


class ParserError(Exception):
    """
    If there's error during construction AST structure from tokens
    """


class FilterParser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = lexer.get_next_token()

    def shift(self, token_type):
        """
        Steps forward and ``eat`` next token with storing it to
        ``self.current_token``

        :rtype: None
        :return: None
        """
        self.current_token = self.lexer.get_next_token()

    def factor(self):
        token = self.current_token
        if token.type in (LITERAL, STRING_LITERAL):
            self.shift(token.type)
            return Literal(token)
        elif token.type == INTEGER:
            self.shift(INTEGER)
            return Num(token)
        elif token.type == MINUS:
            self.shift(MINUS)
            return UnaryOp(token, self.factor())
        elif token.type == LPAREN:
            self.shift(LPAREN)
            node = self.expr()
            self.shift(RPAREN)
            return node
        else:
            raise ParserError("Wrong token: %s" % token.type)

    def term(self):
        term = self.factor()
        while self.current_token.type in HIGH_PRIORITY_OPS:
            token = self.current_token
            self.shift(token.type)
            term = BinOp(left=term, op=token, right=self.factor())
        return term

    def expr(self):
        """
        Parsed node

        :rtype: rtquery.utils.ast.AST
        :return: node
        """
        node = self.term()
        while self.current_token.type in LOW_PRIORITY_OPS:
            token = self.current_token
            self.shift(token.type)
            node = BinOp(left=node, op=token, right=self.term())
        return node

    def parse(self):
        return self.expr()
