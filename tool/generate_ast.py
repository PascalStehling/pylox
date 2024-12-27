import sys

AST_TYPES = [
    "Binary - left: Expr,operator: Token, right: Expr",
    "Grouping - expression: Expr",
    "Literal - value: object",
    "Unary - operator: Token, right: Expr",
]

def define_ast(output_dir: str, base_name: str, types: list[str]):

    contents = []
    contents.append("from dataclasses import dataclass")
    contents.append("from typing import Callable")
    contents.append("")
    contents.append("from lox.token import Token")
    contents.append("")
    contents.append("")
    contents.append("@dataclass")
    contents.append(f"class {base_name}:")
    contents.append('    def accept(self, visitor: "Visitor"):')
    contents.append("        pass")
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
    contents.append('    def accept(self, visitor: "Visitor"):')
    contents.append(f"        return visitor.visit_{class_name.lower()}_{base_name.lower()}(self, visitor)")
    contents.append("")
    contents.append("")
    
    return contents


def define_visitor(contents: list[str], base_name: str, types: list[str]):
    contents.append("@dataclass")
    contents.append("class Visitor:")
    for type in types:
        class_name = type.split("-")[0].strip()
        contents.append(f'    visit_{class_name.lower()}_{base_name.lower()}: Callable[[{class_name}, "Visitor"], None]')
    
    contents.append("")
    


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python generate_ast.py <OUTPUT DIR>")
        sys.exit(64)

    output_dir = sys.argv[1]
    define_ast(output_dir, "Expr", AST_TYPES)
