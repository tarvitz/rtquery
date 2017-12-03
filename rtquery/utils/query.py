from . import parser, lexer, interpreter, visitors

ERROR_LEXER = 0
ERROR_PARSER = 1
ERROR_INTERPRETER = 2
ERROR_VISITOR = 3
ERRORS = (ERROR_LEXER, ERROR_PARSER, ERROR_INTERPRETER, ERROR_VISITOR)


class ReadError(Exception):
    def __init__(self, error_type, error_message):
        self.err_type = error_type
        self.err_message = error_message


def query(text):
    """
    Builds :py:class:`rtquery.Q` object from raw text (user input)

    :param str text: user text input
    :rtype: rtquery.Q
    :return: built queryset
    :raises QueryError: proxies whole processing chain errors and
        encapsulate them into :py:exc:`rtquery.utils.query.ReadError`

    - if :py:exc:`rtquery.utils.lexer.LexerError`
        error appeared during of input tokenization
    - if :py:exc:`rtquery.utils.parser.ParserError`
        error appeared during of ast construction from tokens
    - if :py:exc:`rtquery.utils.interpreter.InterpreterError` error appeared
        during building python objects based on AST structure.
    - if :py:exc:`rtquery.utils.visitors.VisitorError` error appeared during
        composing ast nodes into :py:class:`rtquery.Q` objects
    :raises TypeError: if expression is wrong, for example -"string"
        (instead of -10, -0.5, etc; evaluates from python environment)
    """
    try:
        return interpreter.FilterQueryInterpreter(
            parser.FilterParser(
                lexer.Lexer(text)
            )
        ).interpret()
    except lexer.LexerError as err:
        raise ReadError(error_type=ERROR_LEXER, error_message=err.args[0])
    except parser.ParserError as err:
        raise ReadError(error_type=ERROR_PARSER, error_message=err.args[0])
    except visitors.VisitError as err:
        raise ReadError(error_type=ERROR_VISITOR, error_message=err.args[0])
    except interpreter.InterpreterError as err:
        raise ReadError(error_type=ERROR_INTERPRETER,
                        error_message=err.args[0])
