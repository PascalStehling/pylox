import sys

from lox import Expr
from lox.AstPrinter import AstPrinter
from lox.error import HAD_ERROR, report
from lox.parser import parse
from lox.scanner import scan_tokens
from lox.token import Token
from lox.token_type import TokenType


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
    with open(path, "r") as file:
        content = file.read()

    run(content)

    if HAD_ERROR:
        sys.exit(65)
    


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
    expression = parse(tokens)


    if HAD_ERROR:
        return None

    print(AstPrinter().print(expression))


if __name__ == "__main__":
    main()
