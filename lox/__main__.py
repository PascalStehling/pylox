import sys

# from lox.ast_printer import ast_printer
from lox.Stmt import Stmt
from lox.error import HAD_ERROR, HAD_RUNTIME_ERROR
from lox.interpreter import interpret
from lox.parser import parse
from lox.scanner import scan_tokens


def main():
    if len(sys.argv) > 2:
        print("Usage: python -m lox <SCRIPT>")
        sys.exit(64)
    elif len(sys.argv) == 2:
        print(sys.argv)
        run_file(sys.argv[1])
        pass
    else:
        run_prompt()
        pass


def run_file(path: str):
    global HAD_ERROR
    global HAD_RUNTIME_ERROR
    with open(path, "r") as file:
        content = file.read()

    run(content)

    if HAD_ERROR:
        sys.exit(65)
    if HAD_RUNTIME_ERROR:
        sys.exit(70)
    


def run_prompt():
    global HAD_ERROR
    while True:
        try:
            command = input(":>")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        run(command)
        HAD_ERROR = False


def run(source: str):

    tokens = scan_tokens(source)
    statements: list[Stmt] = parse(tokens)

    if HAD_ERROR:
        return None

    interpret(statements)


if __name__ == "__main__":
    main()
