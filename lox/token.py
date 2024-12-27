# type: ignore
from dataclasses import dataclass
from lox.token_type import TokenType

@dataclass
class Token:
    token_type: TokenType
    lexeme: str
    literal: object | None
    line: int

    def __str__(self):
        return f"{self.token_type} {self.lexeme} {self.literal}"

