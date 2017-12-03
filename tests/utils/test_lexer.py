import unittest

from rtquery.utils.lexer import (
    Lexer, Token, LITERAL, IS, IS_NOT, MATCHES, AND, STRING_LITERAL,
    LPAREN, RPAREN, LexerError
)


class LexerTestCase(unittest.TestCase):
    def test_simple(self):
        text = "Status=new"
        lexer = Lexer(text)
        token = lexer.get_next_token()
        self.assertEqual(token, Token(LITERAL, "Status"))

        token = lexer.get_next_token()
        self.assertEqual(token, Token(IS, "="))

        token = lexer.get_next_token()
        self.assertEqual(token, Token(LITERAL, "new"))

    def test_complex(self):
        text = "CF.{Tags}  ~  release & Status != resolved"
        lexer = Lexer(text)
        token = lexer.get_next_token()
        self.assertEqual(token, Token(LITERAL, 'CF.{Tags}'))

        token = lexer.get_next_token()
        self.assertEqual(token, Token(MATCHES, '~'))

        token = lexer.get_next_token()
        self.assertEqual(token, Token(LITERAL, 'release'))

        token = lexer.get_next_token()
        self.assertEqual(token, Token(AND, '&'))

        token = lexer.get_next_token()
        self.assertEqual(token, Token(LITERAL, 'Status'))

        token = lexer.get_next_token()
        self.assertEqual(token, Token(IS_NOT, '!='))

        token = lexer.get_next_token()
        self.assertEqual(token, Token(LITERAL, 'resolved'))

    def test_string_literal(self):
        text = '"new status for example"'
        lexer = Lexer(text)
        token = lexer.get_next_token()
        self.assertEqual(
            token, Token(STRING_LITERAL, "new status for example")
        )

    def test_string_escaped_literal(self):
        text = r"'there\'s a text'"
        lexer = Lexer(text)
        token = lexer.get_next_token()
        self.assertEqual(
            token, Token(STRING_LITERAL, "there's a text")
        )

    def test_parentheses(self):
        text = "(Status=new | Status=open)"
        lexer = Lexer(text)

        token = lexer.get_next_token()
        self.assertEqual(token, Token(LPAREN, '('))

        while lexer.current_char is not None:
            token = lexer.get_next_token()
        self.assertEqual(token, Token(RPAREN, ')'))

    def test_wrong_not_operation(self):
        text = "Status !% new"
        lexer = Lexer(text)
        with self.assertRaises(LexerError) as err:
            while lexer.current_char is not None:
                lexer.get_next_token()
        self.assertEqual(err.exception.args, ("Wrong operator: !%", ))

    def test_invalid_format(self):
        text = "%%%"
        lexer = Lexer(text)
        with self.assertRaises(LexerError) as err:
            while lexer.current_char is not None:
                lexer.get_next_token()
        self.assertEqual(
            err.exception.args,
            ("Parsing char `%s` at position %i" % ('%', 0), )
        )
