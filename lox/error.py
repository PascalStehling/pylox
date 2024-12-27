
HAD_ERROR = False

def error(line: int, message: str):
    report(line, "", message)


def report(line: int, where: str, message: str):
    global HAD_ERROR
    print(f"[{line}] Error {where}: {message}")

    HAD_ERROR = True
