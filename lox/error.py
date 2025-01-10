from lox.exceptions import RuntimeException

HAD_ERROR = False
HAD_RUNTIME_ERROR = False


def error(line: int, message: str):
    report(line, "", message)


def report(line: int, where: str, message: str):
    global HAD_ERROR
    print(f"[{line}] Error {where}: {message}")

    HAD_ERROR = True


def runtimeError(error: RuntimeException):
    global HAD_RUNTIME_ERROR
    print(f"{error.message}\n[line {error.token.line}]")
    HAD_RUNTIME_ERROR = True
