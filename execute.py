import ply.lex as lex
import ply.yacc as yacc
import gStatLex
import gStatParser
import argparse

# from symbolTable import SymbolTable
# from Quad import Quad

# quads = Quad()

# table = SymbolTable()


lexer = lex.lex(module=gStatLex)
parser = yacc.yacc(module=gStatParser)
parser_prompt = argparse.ArgumentParser()


parser_prompt.add_argument('filepath', help="path to the file")

args = parser_prompt.parse_args()

filename = args.filepath

feed = """"""

with open(filename, 'r') as file:
    for line in file:
        feed += line

parser.parse(feed)

# print()
# print("<-------- SYMBOL TABLE ---------->")
# table.print_symbols()

# print()
# print("<-------- Quads ---------->")
# quad_list = quads.get_quad_list()
# for i, e in enumerate(quad_list):
#     quad = f"{i}: "
#     for elem in e:
#         quad += f" {elem},"
#     print(quad)
