from dataclasses import dataclass
from lox.Enviroment import Environment
from lox.Expr import Assign, Binary, Expr, Grouping, Literal, Unary, ExprVisitor, Variable
from lox.Stmt import Stmt, StmtVisitor, Expression, Var
from lox.error import runtimeError
from lox.exceptions import RuntimeException
from lox.token import Token
from lox.token_type import TokenType


@dataclass
class Visitor(ExprVisitor, StmtVisitor):
    environment = Environment()


def interpret(statements: list[Stmt]):
    interpreter = Visitor(
        visit_binary_expr=visit_binary_expr,  # type: ignore
        visit_grouping_expr=visit_grouping_expr,  # type: ignore
        visit_literal_expr=visit_literal_expr,  # type: ignore
        visit_unary_expr=visit_unary_expr,  # type: ignore
        visit_expression_stmt=visit_expression_stmt,  # type: ignore
        visit_print_stmt=visit_print_stmt,  # type: ignore
        visit_var_stmt=visit_var_stmt,  # type: ignore
        visit_variable_expr=visit_variable_expr,  # type: ignore
        visit_assign_expr=visit_assign_expr)  # type: ignore
    try:
        for statement in statements:
            execute(statement, interpreter)
    except RuntimeException as error:
        runtimeError(error)


def execute(stmt: Stmt, visitor: Visitor):
    stmt.accept(visitor)


def visit_assign_expr(expr: Assign, cursor: Visitor):
    value = evaluate(expr.value, cursor)
    cursor.environment.assign(expr.name, value)
    return value


def visit_variable_expr(expr: Variable, visitor: Visitor):
    return visitor.environment.get(expr.name)


def visit_var_stmt(stmt: Var, visitor: Visitor):
    value = None
    if stmt.initializer is not None:
        value = evaluate(stmt.initializer, visitor)

    visitor.environment.define(stmt.name.lexeme, value)
    return None


def visit_expression_stmt(stmt: Expression, visitor: Visitor):
    evaluate(stmt.expression, visitor)


def visit_print_stmt(stmt: Expression, visitor: Visitor):
    value = evaluate(stmt.expression, visitor)
    print(stringify(value))


def visit_literal_expr(expr: Literal, _: Visitor):
    return expr.value


def visit_grouping_expr(expr: Grouping, visitor: Visitor):
    return evaluate(expr.expression, visitor)


def visit_unary_expr(expr: Unary, visitor: Visitor) -> float:
    right = evaluate(expr.right, visitor)

    if expr.operator.token_type == TokenType.BANG:
        return not is_truthy(right)
    if expr.operator.token_type == TokenType.MINUS:
        check_number_operand(expr.operator, right)
        return -float(right)  # type: ignore

    # Unreachable
    return None  # type: ignore


def visit_binary_expr(expr: Binary, visitor: Visitor):
    left = evaluate(expr.left, visitor)
    right = evaluate(expr.right, visitor)

    match expr.operator.token_type:
        case TokenType.GREATER:
            check_number_operands(expr.operator, left, right)
            return float(left) > float(right)  # type: ignore
        case TokenType.GREATER_EQUAL:
            check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)  # type: ignore
        case TokenType.LESS:
            check_number_operands(expr.operator, left, right)
            return float(left) < float(right)  # type: ignore
        case TokenType.LESS_EQUAL:
            check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)  # type: ignore
        case TokenType.EQUAL_EQUAL:
            return is_equal(left, right)
        case TokenType.BANG_EQUAL:
            return not is_equal(left, right)
        case TokenType.MINUS:
            check_number_operands(expr.operator, left, right)
            return float(left) - float(right)  # type: ignore
        case TokenType.PLUS:
            # I know this is unnecessary as python does the same thing already by nature
            # so just + would be enough, but this is for educational purpose
            if isinstance(left, float) and isinstance(right, float):
                check_number_operands(expr.operator, left, right)
                return float(left) + float(right)
            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
        case TokenType.SLASH:
            check_number_operands(expr.operator, left, right)
            return float(left) / float(right)  # type: ignore
        case TokenType.STAR:
            check_number_operands(expr.operator, left, right)
            return float(left) * float(right)  # type: ignore

    # Unreachable
    return None


def evaluate(expr: Expr, visitor: Visitor):
    return expr.accept(visitor)


def is_truthy(value: object) -> bool:
    if value is None:
        return False
    if isinstance(value, bool):
        return value

    return True


def is_equal(a: object, b: object) -> bool:
    if a is None and b is None:
        return True
    if a is None:
        return False

    return a == b


def check_number_operand(operator: Token, operand: object):
    if isinstance(operand, float):
        return
    raise RuntimeException(operator, "Must be a number")


def check_number_operands(operator: Token, left: object, right: object):
    if isinstance(left, float) and isinstance(right, float):
        return

    raise RuntimeException(operator, "Operands must be a numbers")


def stringify(obj: object):
    if obj is None:
        return "nil"

    if isinstance(obj, float):
        text = str(obj)
        if text.endswith(".0"):
            text = text[:-2]
        return text

    return str(obj)
