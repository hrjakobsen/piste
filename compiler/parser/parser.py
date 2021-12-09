from antlr4 import FileStream, CommonTokenStream, InputStream

from parser.auto.pisteLexer import pisteLexer
from parser.auto.pisteParser import pisteParser
from parser.coretransformer import CoreBuilder


def parse_file(filename):
    input_stream = FileStream(filename)
    return parse_stream(input_stream)


def parse_string(str):
    input_stream = InputStream(str)
    return parse_stream(input_stream)


def parse_stream(input_stream):
    lexer = pisteLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = pisteParser(token_stream)
    tree = parser.program()
    ast_builder = CoreBuilder()
    return tree.accept(ast_builder)


