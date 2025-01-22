from dataclasses import dataclass
from typing import Any, Callable

from lox.Expr import Expr
from lox.token import Token


@dataclass
class Stmt:
    def accept(self, visitor: "StmtVisitor")-> "Stmt":
        return Stmt()


@dataclass
class Expression(Stmt):
    expression: Expr

    def accept(self, visitor: "StmtVisitor") -> "Stmt":
        return visitor.visit_expression_stmt(self, visitor)


@dataclass
class Print(Stmt):
    expression: Expr

    def accept(self, visitor: "StmtVisitor") -> "Stmt":
        return visitor.visit_print_stmt(self, visitor)


@dataclass
class Var(Stmt):
    name: Token
    initializer: Expr | None

    def accept(self, visitor: "StmtVisitor") -> "Stmt":
        return visitor.visit_var_stmt(self, visitor)


@dataclass
class StmtVisitor:
    visit_expression_stmt: Callable[[Expression, "StmtVisitor"], Any]
    visit_print_stmt: Callable[[Print, "StmtVisitor"], Any]
    visit_var_stmt: Callable[[Var, "StmtVisitor"], Any]

