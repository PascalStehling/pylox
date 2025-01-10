from lox.Expr import Binary, Expr, Grouping, Literal, Unary, Visitor
from lox.error import runtimeError
from lox.exceptions import RuntimeException
from lox.token import Token
from lox.token_type import TokenType


def interpret(expression: Expr):
    interpreter = Visitor(visit_binary_expr=visit_binary_expr,
                          visit_grouping_expr=visit_grouping_expr,
                          visit_literal_expr=visit_literal_expr,
                          visit_unary_expr=visit_unary_expr)
    try:
        result = expression.accept(interpreter)
        return stringify(result)
    except RuntimeException as error:
        runtimeError(error)


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
        return -float(right)

    # Unreachable
    return None


def visit_binary_expr(expr: Binary, visitor:Visitor):
    left = evaluate(expr.left, visitor)
    right = evaluate(expr.right, visitor)

    match expr.operator.token_type:
        case TokenType.GREATER:
            check_number_operands(expr.operator, left, right)
            return float(left) > float(right)
        case TokenType.GREATER_EQUAL:
            check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)
        case TokenType.LESS:
            check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        case TokenType.LESS_EQUAL:
            check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)
        case TokenType.EQUAL_EQUAL:
            return is_equal(left, right)
        case TokenType.BANG_EQUAL:
            return not is_equal(left, right)
        case TokenType.MINUS:
            check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
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
            return float(left) / float(right)
        case TokenType.STAR:
            check_number_operands(expr.operator, left, right)
            return float(left) * float(right)

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