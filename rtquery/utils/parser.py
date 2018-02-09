from . consts import (
    LITERAL, STRING_LITERAL, LPAREN, INTEGER, MINUS,
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

    def shift(self):
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
            self.shift()
            return Literal(token)
        elif token.type == STRING_LITERAL:
            self.shift()
            return StringLiteral(token)
        elif token.type == MINUS:
            self.shift()
            return UnaryOp(op=token, expr=self.composite())
        elif token.type == INTEGER:
            self.shift()
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
        self.shift()

        op_token = self.current_token
        if op_token.type not in HIGH_PRIORITY_OPS:
            raise ParserError(
                "Wrong operation %r for statement given" % op_token.type
            )
        self.shift()
        right = self.composite()
        return BinOp(left=Literal(token), op=op_token, right=right)

    def statement_group(self):
        if self.current_token.type == LPAREN:
            self.shift()
            node = self.statement_group()
            self.shift()
            return node

        statement = self.statement()
        while self.current_token.type in LOW_PRIORITY_OPS:
            token = self.current_token
            self.shift()
            if self.current_token.type == LPAREN:
                rhs_statement = self.statement_group()
            else:
                rhs_statement = self.statement()
            statement = BinOp(left=statement, op=token, right=rhs_statement)
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
            self.shift()
            node = BinOp(left=node, op=token, right=self.statement_group())
        return node

    def parse(self):
        return self.expression()
