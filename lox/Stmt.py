from dataclasses import dataclass
from typing import Callable

from lox.Expr import Expr


@dataclass
class Stmt:
    def accept(self, visitor: "StmtVisitor"):
        pass


@dataclass
class Expression(Stmt):
    expression: Expr

    def accept(self, visitor: "StmtVisitor"):
        return visitor.visit_expression_stmt(self, visitor)


@dataclass
class Print(Stmt):
    expression: Expr

    def accept(self, visitor: "StmtVisitor"):
        return visitor.visit_print_stmt(self, visitor)


@dataclass
class StmtVisitor:
    visit_expression_stmt: Callable[[Expression, "StmtVisitor"], None]
    visit_print_stmt: Callable[[Print, "StmtVisitor"], None]

