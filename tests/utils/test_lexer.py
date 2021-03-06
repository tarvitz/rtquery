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
        text = "CF_Tags  ~  release-on-prod & Status != resolved"
        lexer = Lexer(text)
        token = lexer.get_next_token()
        self.assertEqual(token, Token(LITERAL, 'CF_Tags'))

        token = lexer.get_next_token()
        self.assertEqual(token, Token(MATCHES, '~'))

        token = lexer.get_next_token()
        self.assertEqual(token, Token(LITERAL, 'release-on-prod'))

        token = lexer.get_next_token()
        self.assertEqual(token, Token(AND, '&'))

        token = lexer.get_next_token()
        self.assertEqual(token, Token(LITERAL, 'Status'))

        token = lexer.get_next_token()
        self.assertEqual(token, Token(IS_NOT, '!='))

        token = lexer.get_next_token()
        self.assertEqual(token, Token(LITERAL, 'resolved'))

    def test_complex_with_string_literal(self):
        text = "Queue='complex-queue' & Status != resolved"
        lexer = Lexer(text)
        count = 0
        last_token = None
        while lexer.current_char is not None:
            last_token = lexer.get_next_token()
            count += 1
        self.assertEqual(count, 7)
        self.assertIsInstance(last_token, Token)
        self.assertEqual(last_token, Token(LITERAL, "resolved"))

    def test_literal(self):
        text = 'Queue = composite-literal'
        lexer = Lexer(text)
        token = None
        while lexer.current_char is not None:
            token = lexer.get_next_token()
        self.assertEqual(token, Token(LITERAL, 'composite-literal'))

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
        self.assertEqual(err.exception.args,
                         ('Parsing char `!` at position 7', ))

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

    def test_invalid_format_peek_is_None(self):
        text = '!'
        lexer = Lexer(text)
        with self.assertRaises(LexerError) as err:
            while lexer.current_char is not None:
                lexer.get_next_token()
        self.assertEqual(
            err.exception.args,
            ('Parsing char `!` at position 0',)
        )

    def test_blank_string_literal(self):
        text = '""'
        lexer = Lexer(text)
        token = lexer.get_next_token()
        self.assertEqual(token, Token(STRING_LITERAL, ''))

    def test_iter(self):
        text = 'Status ~ open & (Test ~ message | Owner = user)'
        tokens = [x for x in Lexer(text)]
        self.assertEqual(len(tokens), 13)
        self.assertEqual(tokens[0], Token(LITERAL, 'Status'))
        self.assertEqual(tokens[-1], Token(RPAREN, ')'))
