
from lox.error import report
from lox.token import Token
from lox.token_type import TokenType


def error(token: Token, message: str):
    if token.token_type == TokenType.EOF:
        report(token.line, " at end", message)
    else:
        report(token.line, f"at '{token.lexeme}'", message)

