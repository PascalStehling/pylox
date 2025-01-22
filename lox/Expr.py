from dataclasses import dataclass
from typing import Any, Callable

from lox.token import Token


@dataclass
class Expr:
    def accept(self, visitor: "ExprVisitor")-> "Expr":
        return Expr()


@dataclass
class Assign(Expr):
    name: Token
    value: Expr

    def accept(self, visitor: "ExprVisitor") -> "Expr":
        return visitor.visit_assign_expr(self, visitor)


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: "ExprVisitor") -> "Expr":
        return visitor.visit_binary_expr(self, visitor)


@dataclass
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor: "ExprVisitor") -> "Expr":
        return visitor.visit_grouping_expr(self, visitor)


@dataclass
class Literal(Expr):
    value: object

    def accept(self, visitor: "ExprVisitor") -> "Expr":
        return visitor.visit_literal_expr(self, visitor)


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor: "ExprVisitor") -> "Expr":
        return visitor.visit_unary_expr(self, visitor)


@dataclass
class Variable(Expr):
    name: Token

    def accept(self, visitor: "ExprVisitor") -> "Expr":
        return visitor.visit_variable_expr(self, visitor)


@dataclass
class ExprVisitor:
    visit_assign_expr: Callable[[Assign, "ExprVisitor"], Any]
    visit_binary_expr: Callable[[Binary, "ExprVisitor"], Any]
    visit_grouping_expr: Callable[[Grouping, "ExprVisitor"], Any]
    visit_literal_expr: Callable[[Literal, "ExprVisitor"], Any]
    visit_unary_expr: Callable[[Unary, "ExprVisitor"], Any]
    visit_variable_expr: Callable[[Variable, "ExprVisitor"], Any]

