from . consts import (
    LITERAL, STRING_LITERAL, LPAREN, RPAREN, INTEGER, MINUS,
    LOW_PRIORITY_OPS, HIGH_PRIORITY_OPS
)

from . ast import Literal, StringLiteral, BinOp, Num, UnaryOp


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

    def composite(self):
        token = self.current_token
        if token.type == LITERAL:
            self.shift(token.type)
            return Literal(token)
        elif token.type == STRING_LITERAL:
            self.shift(token.type)
            return StringLiteral(token)
        elif token.type == MINUS:
            self.shift(token.type)
            return UnaryOp(op=token, expr=self.composite())
        elif token.type == INTEGER:
            self.shift(token.type)
            return Num(token)
        else:
            raise ParserError("Wrong statement right part: '%r'" % token)

    def statement(self):
        token = self.current_token
        if token.type not in (LITERAL, STRING_LITERAL):
            raise ParserError(
                "Statement should start with Literal or StringLiteral, "
                "'%r' given" % token
            )
        self.shift(token.type)

        op_token = self.current_token
        if op_token.type not in HIGH_PRIORITY_OPS:
            raise ParserError(
                "Wrong operation %r for statement given" % op_token.type
            )
        self.shift(op_token.type)
        right = self.composite()
        return BinOp(left=Literal(token), op=op_token, right=right)

    def statement_group(self):
        if self.current_token.type == LPAREN:
            self.shift(LPAREN)
            node = self.statement_group()
            self.shift(RPAREN)
            return node

        statement = self.statement()
        while self.current_token.type in LOW_PRIORITY_OPS:
            token = self.current_token
            self.shift(token.type)
            statement = BinOp(left=statement, op=token, right=self.statement())
        return statement

    def expression(self):
        """
        Parsed node

        :rtype: rtquery.utils.ast.AST
        :return: node
        """
        node = self.statement_group()
        while self.current_token.type in LOW_PRIORITY_OPS:
            token = self.current_token
            self.shift(token.type)
            node = BinOp(left=node, op=token, right=self.statement_group())
        return node

    def parse(self):
        return self.expression()
