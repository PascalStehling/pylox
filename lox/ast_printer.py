from lox import Expr

def ast_printer(expression: Expr.Expr):

    printer = Expr.Visitor(visit_binary_expr=visit_binary_expr,
                           visit_grouping_expr=visit_grouping_expr,
                           visit_literal_expr=visit_literal_expr,
                           visit_unary_expr=visit_unary_expr)
    return expression.accept(printer)


def visit_binary_expr(expr: Expr.Binary, visitor: Expr.Visitor):
    return parenthesize(visitor, expr.operator.lexeme, expr.left, expr.right)


def visit_grouping_expr(expr: Expr.Grouping, visitor: Expr.Visitor):
    return parenthesize(visitor, "group", expr.expression)


def visit_literal_expr(expr: Expr.Literal, visitor: Expr.Visitor):
    if expr.value is None:
        return "nil"
    return str(expr.value)


def visit_unary_expr(expr: Expr.Unary, visitor: Expr.Visitor):
    return parenthesize(visitor, expr.operator.lexeme, expr.right)


def parenthesize(visitor: Expr.Visitor, name: str, *exprs: Expr.Expr):
    string = ""
    string += f"({name}"
    for expr in exprs:
        string += f" {expr.accept(visitor)}"
    string += ")"

    return string
