from ast import literal_eval

from . ast import Token
from . consts import (
    LITERAL, GREAT_THAN, LESS_THAN, MATCHES, MATCHES_NOT, IS, IS_NOT, AND, OR,
    MINUS,
    LPAREN, RPAREN, STRING_LITERAL, INTEGER, EOF
)


class LexerError(Exception):
    """
    Lexer Error, uses to identify wrong text to tokenize
    """


class Lexer(object):
    """
    Tokenize user input text
    """
    def __init__(self, text: str):
        self.text = text

        #: current position of text tokenize
        self.pos = 0
        self.current_char = self.text[self.pos]

    def advance(self, forward=1):
        """
        Advance the ``pos`` pointer and set the ``current_char`` variable.

        :param int forward: amount of steps forward
        :rtype: None
        :return: None
        """
        self.pos += forward
        if self.pos > len(self.text) - 1:  # EOF
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        """
        Returns a next character after current position

        :rtype: str | None
        :return:
        """
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while (self.current_char is not None
               and self.current_char.isspace()):
            self.advance()

    def literal(self):
        """Return a string literal consumed from input"""
        result = ''
        valid_sequence = ['_', '-']
        while (self.current_char is not None
               and (self.current_char.isalnum()
                    or self.current_char in valid_sequence)):
            result += self.current_char
            self.advance()
        return result

    def string_literal(self):
        result = ''
        terminal_symbol = self.current_char
        self.advance()
        while (self.current_char is not None and
                self.current_char != terminal_symbol):
            result += self.current_char
            self.advance()

            #: pass through escaped chars
            if self.current_char == '\\':
                self.advance()
                result += literal_eval('"\\%s"' % self.current_char)
                self.advance()
        self.advance()
        return result

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def error(self, msg=None):
        raise LexerError(msg or "Lexing process caught an error")

    def get_next_token(self):
        """
        Reads text forward and chunks it with tokens

        :rtype: rtquery.utils.ast.Token
        :return: next read token
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha():
                return Token(LITERAL, self.literal())

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char in ("'", '"'):
                return Token(
                    STRING_LITERAL,
                    self.string_literal()
                )

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')
            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == '>':
                self.advance()
                return Token(GREAT_THAN, '>')

            if self.current_char == '<':
                self.advance()
                return Token(LESS_THAN, '<')

            if self.current_char == '~':
                self.advance()
                return Token(MATCHES, '~')
            if self.current_char == '=':
                self.advance()
                return Token(IS, '=')

            if self.current_char == '!' and self.peek() == '=':
                self.advance(2)
                return Token(IS_NOT, '!=')

            if self.current_char == '!' and self.peek() == '~':
                self.advance(2)
                return Token(MATCHES_NOT, '!~')

            if self.current_char == '|':
                self.advance()
                return Token(OR, '|')
            if self.current_char == '&':
                self.advance()
                return Token(AND, '&')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            self.error(
                "Parsing char `%s` at position %i" % (
                    self.current_char, self.pos
                )
            )
        return Token(EOF, None)
