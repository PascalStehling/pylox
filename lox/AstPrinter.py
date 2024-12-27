

from lox import Expr


class AstPrinter(Expr.Visitor):

    def print(self, expr: Expr.Expr):
        return expr.accept(self)

    def visit_binary_expr(self, expr:Expr.Binary):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: Expr.Grouping):
        return self.parenthesize("group", expr.expression)
    
    def visit_literal_expr(self, expr: Expr.Literal):
        if expr.value is None:
            return "nil"
        return str(expr.value)
    
    def visit_unary_expr(self, expr: Expr.Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)
    
    def parenthesize(self, name: str, *exprs: Expr.Expr):
        string = ""
        string += f"({name}"
        for expr in exprs:
            string += f" {expr.accept(self)}"
        string += ")"

        return string