import subprocess

from ccodegen import generate_c_code
from parser.core import ExternalDeclaration, ExternProcessNode
from parser.first_pass import pass_one
from parser.parser import parse_file
import sys
import tempfile
from pathlib import Path

from printer import PrinterVisitor
from typechecker import TypeCheckerVisitor

PISTE_PATH = Path.home().joinpath(".piste")


def add_decls(ast, decls):
    if len(decls) == 0:
        return ast
    decl = decls[0]
    decls = decls[1:]
    if not isinstance(decl, ExternalDeclaration):
        raise Exception("Declaration type unsupported")
    following = add_decls(ast, decls)
    extended = ExternProcessNode(
        decl.external_name,
        decl.arg_types,
        decl.ret_type,
        decl.internal_name,
        following
    )
    return extended


def main():
    ast, decls = (parse_file(sys.argv[1]))
    ast = add_decls(ast, decls)
    pass_one(ast)
    if "--skip-typechecking" not in sys.argv:
        ast.accept(TypeCheckerVisitor(decls))
    print(ast.accept(PrinterVisitor()))
    code = generate_c_code(ast)
    if "--print-c" in sys.argv:
        print(code)
    compiled_file = compile_code(code)
    execute_file(compiled_file)


def compile_code(source):
    directory = tempfile.mkdtemp()
    file_path = directory + "/" + "program.c"
    with open(file_path, "w") as file:
        file.write(source)
        file.close()
    gcc_call = [
        "gcc",
        "-iquote", str(PISTE_PATH.joinpath("include").absolute()),
        file_path, "-L", str(PISTE_PATH.joinpath("lib").absolute()),
        "-lpiste",
        "-lpiste_std",
        "-lm", # link with math library
        "-o" + directory + "/program"
    ]
    print("Using gcc command: " + " ".join(gcc_call))
    subprocess.run(gcc_call, check=True)
    return directory + "/program"


def execute_file(file):
    subprocess.run(file, check=True)


if __name__ == "__main__":
    main()
