from lox.exceptions import RuntimeException
from lox.token import Token


class Environment:
    values: dict = {}

    def define(self, name: str, value: object):
        self.values[name] = value

    def get(self, name: Token) -> object:
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        raise RuntimeException(name, f"Undefined variable {name.lexeme}.")

    def assign(self, name: Token, value: object):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        raise RuntimeException(name, f"Undefined variable {name.lexeme}.")
