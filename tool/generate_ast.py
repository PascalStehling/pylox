import sys

EXPR_TYPES = [
    "Assign - name: Token, value: Expr",
    "Binary - left: Expr, operator: Token, right: Expr",
    "Grouping - expression: Expr",
    "Literal - value: object",
    "Unary - operator: Token, right: Expr",
    "Variable - name: Token"
]

STATEMENT_TYPES = [
    "Expression - expression: Expr",
    "Print - expression: Expr",
    "Var - name: Token, initializer: Expr | None"
]

def define_ast(output_dir: str, base_name: str, types: list[str]):

    contents = []
    contents.append("from dataclasses import dataclass")
    contents.append("from typing import Any, Callable")
    contents.append("")
    contents.append("from lox.token import Token")
    contents.append("")
    contents.append("")
    contents.append("@dataclass")
    contents.append(f"class {base_name}:")
    contents.append(f'    def accept(self, visitor: "{base_name}Visitor")-> "{base_name}":')
    contents.append(f"        return {base_name}()")
    contents.append("")
    contents.append("")

    for type in types:
        class_name = type.split("-")[0].strip()
        fields = type.split("-")[1].strip()

        define_type(contents, base_name, class_name, fields)

    define_visitor(contents, base_name, types)

    file_path = f"{output_dir}/{base_name}.py"
    with open(file_path, "+w") as file:
        contents = [c+"\n" for c in contents]
        file.writelines(contents)


def define_type(contents: list[str], base_name: str, class_name: str, fields: str):
    contents.append("@dataclass")
    contents.append(f"class {class_name}({base_name}):")
    for field in fields.split(","):
        contents.append(f"    {field.strip()}")
    
    contents.append("")
    contents.append(f'    def accept(self, visitor: "{base_name}Visitor") -> "{base_name}":')
    contents.append(f"        return visitor.visit_{class_name.lower()}_{base_name.lower()}(self, visitor)")
    contents.append("")
    contents.append("")
    
    return contents


def define_visitor(contents: list[str], base_name: str, types: list[str]):
    contents.append("@dataclass")
    contents.append(f"class {base_name}Visitor:")
    for type in types:
        class_name = type.split("-")[0].strip()
        contents.append(f'    visit_{class_name.lower()}_{base_name.lower()}: Callable[[{class_name}, "{base_name}Visitor"], Any]')
    
    contents.append("")
    


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python generate_ast.py <OUTPUT DIR>")
        sys.exit(64)

    output_dir = sys.argv[1]
    define_ast(output_dir, "Expr", EXPR_TYPES)
    define_ast(output_dir, "Stmt", STATEMENT_TYPES)
