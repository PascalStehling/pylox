from dataclasses import dataclass
from typing import Callable

from lox.token import Token


@dataclass
class Expr:
    def accept(self, visitor: "ExprVisitor"):
        pass


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: "ExprVisitor"):
        return visitor.visit_binary_expr(self, visitor)


@dataclass
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor: "ExprVisitor"):
        return visitor.visit_grouping_expr(self, visitor)


@dataclass
class Literal(Expr):
    value: object

    def accept(self, visitor: "ExprVisitor"):
        return visitor.visit_literal_expr(self, visitor)


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor: "ExprVisitor"):
        return visitor.visit_unary_expr(self, visitor)


@dataclass
class ExprVisitor:
    visit_binary_expr: Callable[[Binary, "ExprVisitor"], None]
    visit_grouping_expr: Callable[[Grouping, "ExprVisitor"], None]
    visit_literal_expr: Callable[[Literal, "ExprVisitor"], None]
    visit_unary_expr: Callable[[Unary, "ExprVisitor"], None]

