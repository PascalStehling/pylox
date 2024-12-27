from dataclasses import dataclass

from lox.token import Token


@dataclass
class Expr:
    def accept(self, visitor: "Visitor"):
        pass


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: "Visitor"):
        return visitor.visit_binary_expr(self)


@dataclass
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor: "Visitor"):
        return visitor.visit_grouping_expr(self)


@dataclass
class Literal(Expr):
    value: object

    def accept(self, visitor: "Visitor"):
        return visitor.visit_literal_expr(self)


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor: "Visitor"):
        return visitor.visit_unary_expr(self)


class Visitor:
    def visit_binary_expr(self, expr: Binary):
        pass
    def visit_grouping_expr(self, expr: Grouping):
        pass
    def visit_literal_expr(self, expr: Literal):
        pass
    def visit_unary_expr(self, expr: Unary):
        pass

