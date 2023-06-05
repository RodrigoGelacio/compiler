import ply.lex as lex
import ply.yacc as yacc
import gStatLex
import gStatParser
from symbolTable import SymbolTable
from Quad import Quad

quads = Quad()

table = SymbolTable()


lexer = lex.lex(module=gStatLex)
parser = yacc.yacc(module=gStatParser)

ex = r"""
program lol;

main(){

    float i;

    read(i);

    print(i);

}
"""

result = parser.parse(ex)
print()
print("<-------- SYMBOL TABLE ---------->")
table.print_symbols()

print()
print("<-------- Quads ---------->")
quad_list = quads.get_quad_list()
for i, e in enumerate(quad_list):
    quad = f"{i}: "
    for elem in e:
        quad += f" {elem},"
    print(quad)
