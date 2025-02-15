from dataclasses import dataclass
from lox import Expr
from lox import Stmt
import lox
from lox.token import Token
from lox.token_type import TokenType


class ParseError(Exception):
    pass


@dataclass
class Cursor:
    tokens: list[Token]
    current: int = 0


def parse(tokens: list[Token]):
    cursor = Cursor(tokens)
    statements: list[Stmt.Stmt | None] = []
    while not is_at_end(cursor):
        statements.append(declaration(cursor))
    return statements


def declaration(cursor: Cursor) -> Stmt.Stmt | None:
    try:
        if match(cursor, TokenType.VAR):
            return var_declaration(cursor)
        return statement(cursor)
    except ParseError:
        synchronize(cursor)
        return None


def var_declaration(cursor: Cursor):
    name = consume(cursor, TokenType.IDENTIFIER, "Expect variable name.")

    initializer = None
    if match(cursor, TokenType.EQUAL):
        initializer = expression(cursor)

    consume(cursor, TokenType.SEMICOLON,
            "Expect ';' after variable declaration")

    return Stmt.Var(name, initializer)


def statement(cursor: Cursor) -> Stmt.Stmt:
    if match(cursor, TokenType.PRINT):
        return printStatement(cursor)
    return expressionStatement(cursor)


def printStatement(cursor: Cursor):
    value = expression(cursor)
    consume(cursor, TokenType.SEMICOLON, "Expect ';' after value")
    return Stmt.Print(value)


def expressionStatement(cursor: Cursor):
    expr = expression(cursor)
    consume(cursor, TokenType.SEMICOLON, "Expect ';' after expression")
    return Stmt.Expression(expr)


def expression(cursor: Cursor) -> Expr.Expr:
    return assignment(cursor)


def assignment(cursor: Cursor) -> Expr.Expr:
    expr = equality(cursor)

    if match(cursor, TokenType.EQUAL):
        equals = previous(cursor)
        value = assignment(cursor)
        if isinstance(expr, Expr.Variable):
            name = expr.name
            return Expr.Assign(name, value)

        error(equals, "Invalid Assignment Target")

    return expr


def equality(cursor: Cursor):
    expr = comparison(cursor)

    while match(cursor, TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
        operator = previous(cursor)
        right = comparison(cursor)
        expr = Expr.Binary(expr, operator, right)

    return expr


def comparison(cursor: Cursor):
    expr = term(cursor)

    while match(cursor, TokenType.GREATER, TokenType.GREATER_EQUAL,
                TokenType.LESS, TokenType.LESS_EQUAL):
        operator = previous(cursor)
        right = term(cursor)
        expr = Expr.Binary(expr, operator, right)

    return expr


def term(cursor: Cursor):
    expr = factor(cursor)

    while match(cursor, TokenType.MINUS, TokenType.PLUS):
        operator = previous(cursor)
        right = factor(cursor)

        expr = Expr.Binary(expr, operator, right)

    return expr


def factor(cursor: Cursor):
    expr = unary(cursor)

    while match(cursor, TokenType.SLASH, TokenType.STAR):
        operator = previous(cursor)
        right = unary(cursor)
        expr = Expr.Binary(expr, operator, right)

    return expr


def unary(cursor: Cursor):
    if match(cursor, TokenType.BANG, TokenType.MINUS):
        operator = previous(cursor)
        right = unary(cursor)
        return Expr.Unary(operator, right)

    return primary(cursor)


def primary(cursor: Cursor):
    if match(cursor, TokenType.FALSE):
        return Expr.Literal(False)
    if match(cursor, TokenType.TRUE):
        return Expr.Literal(True)
    if match(cursor, TokenType.NIL):
        return Expr.Literal(None)

    if match(cursor, TokenType.NUMBER, TokenType.STRING):
        return Expr.Literal(previous(cursor).literal)

    if match(cursor, TokenType.IDENTIFIER):
        return Expr.Variable(previous(cursor))

    if match(cursor, TokenType.LEFT_PAREN):
        expr = expression(cursor)
        consume(cursor, TokenType.RIGHT_PAREN, "Expected ) after expression")
        return Expr.Grouping(expr)

    raise error(peek(cursor), "Expected Expression")


def consume(cursor: Cursor, type: TokenType, message: str):
    if check(cursor, type):
        return advance(cursor)

    raise error(peek(cursor), message)


def error(token: Token, message: str):
    lox.error(token, message)
    return ParseError()


def synchronize(cursor: Cursor):
    advance(cursor)
    while not is_at_end(cursor):
        if previous(cursor) == TokenType.SEMICOLON:
            return
        match peek(cursor).token_type:
            case (TokenType.CLASS | TokenType.FUN | TokenType.VAR
                  | TokenType.FOR | TokenType.IF | TokenType.WHILE
                  | TokenType.PRINT | TokenType.RETURN):
                return
        advance(cursor)


def match(cursor: Cursor, *types: TokenType):
    for type in types:
        if check(cursor, type):
            advance(cursor)
            return True

    return False


def check(cursor: Cursor, type: TokenType):
    if is_at_end(cursor):
        return False

    return peek(cursor).token_type == type


def advance(cursor: Cursor) -> Token:
    if not is_at_end(cursor):
        cursor.current += 1
    return previous(cursor)


def is_at_end(cursor: Cursor) -> bool:
    return peek(cursor).token_type == TokenType.EOF


def peek(cursor: Cursor) -> Token:
    return cursor.tokens[cursor.current]


def previous(cursor: Cursor) -> Token:
    return cursor.tokens[cursor.current - 1]
