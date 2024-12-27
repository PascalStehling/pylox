from dataclasses import dataclass
from lox.error import error
from lox.token import Token
from lox.token_type import KEYWORDS, TokenType


@dataclass
class Cursor:
    source: str
    current: int = 0
    start: int = 0
    line: int = 1

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False

        if expected != self.source[self.current]:
            return False

        self.current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def peekNext(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]


def scan_tokens(source: str) -> list[Token]:
    cursor = Cursor(source)
    tokens: list[Token] = []

    while not cursor.is_at_end():
        cursor.start = cursor.current
        token = scan_token(cursor)
        if token is None:
            continue
        tokens.append(token)

    tokens.append(Token(TokenType.EOF, "", None, cursor.line))
    return tokens


def scan_token(cursor: Cursor):
    char = cursor.advance()

    match char:
    # Single Letter matches
        case "(":
            return create_token(cursor, TokenType.LEFT_PAREN)
        case ")":
            return create_token(cursor, TokenType.RIGHT_PAREN)
        case "{":
            return create_token(cursor, TokenType.LEFT_BRACE)
        case "}":
            return create_token(cursor, TokenType.RIGHT_BRACE)
        case ",":
            return create_token(cursor, TokenType.COMMA)
        case ".":
            return create_token(cursor, TokenType.DOT)
        case "-":
            return create_token(cursor, TokenType.MINUS)
        case "+":
            return create_token(cursor, TokenType.PLUS)
        case ";":
            return create_token(cursor, TokenType.SEMICOLON)
        case "*":
            return create_token(cursor, TokenType.STAR)
        # One or Two letter matches
        case "!":
            return create_token(
                cursor,
                TokenType.BANG_EQUAL if cursor.match("=") else TokenType.BANG)
        case "=":
            return create_token(
                cursor, TokenType.EQUAL_EQUAL
                if cursor.match("=") else TokenType.EQUAL)
        case "<":
            return create_token(
                cursor,
                TokenType.LESS_EQUAL if cursor.match("=") else TokenType.LESS)
        case ">":
            return create_token(
                cursor, TokenType.GREATER_EQUAL
                if cursor.match("=") else TokenType.GREATER)
        case "/":
            if cursor.match("/"):
                while cursor.peek() != "\0":
                    cursor.advance()
                return None
            else:
                return create_token(cursor, TokenType.SLASH)

        # Special Characters
        case " " | "\r" | "\t":
            # Ignore Whitespace
            return None
        case "\n":
            cursor.line += 1
            return None

        case '"':
            return extract_string_token(cursor)

        case _:
            if is_digit(char):
                return extract_number_token(cursor)

            if is_alpha(char):
                return extract_identifier_token(char)

            error(cursor.line, "Unexpected Character")
            return


def extract_string_token(cursor: Cursor) -> Token:
    while cursor.peek() != '"' and not cursor.is_at_end():
        if cursor.peek() == "\n":
            cursor.line += 1
        cursor.advance()

    if cursor.is_at_end():
        error(cursor.line, "Unterminated String")
        return None

    # the closing "
    cursor.advance()

    value = cursor.source[cursor.start + 1: cursor.current - 1]
    return create_token(cursor, TokenType.STRING, value)


def extract_number_token(cursor: Cursor) -> Token:
    while is_digit(cursor.peek()):
        cursor.advance()

    if cursor.peek() == "." and is_digit(cursor.peekNext()):
        cursor.advance()
        while is_digit(cursor.peek()):
            cursor.advance()

    return create_token(cursor, TokenType.NUMBER,
                        float(cursor.source[cursor.start: cursor.current]))


def extract_identifier_token(cursor: Cursor) -> Token:
    while is_alpha_num(cursor.peek()):
        cursor.advance()

    text = cursor.source[cursor.start: cursor.current]
    token_type = KEYWORDS.get(text)
    if token_type is None:
        token_type = TokenType.IDENTIFIER

    return create_token(cursor, token_type)


def is_digit(char: str) -> bool:
    return char >= '0' and char <= '9'


def is_alpha(char: str) -> bool:
    return ((char >= "a" and char <= "z") or (char >= "A" and char <= "Z")
            or char == "_")


def is_alpha_num(char: str) -> bool:
    return is_digit(char) or is_alpha(char)


def create_token(cursor: Cursor,
                 token_type: TokenType,
                 literal: object | None = None):
    return Token(token_type, cursor.source[cursor.start: cursor.current],
                 literal, cursor.line)
