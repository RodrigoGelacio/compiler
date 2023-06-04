import ply.lex as lex
import ply.yacc as yacc
import my_lexer
import my_parser
from symbolTable import SymbolTable
from Quad import Quad

quads = Quad()

table = SymbolTable()


lexer = lex.lex(module=my_lexer)
parser = yacc.yacc(module=my_parser)

ex = r"""
program lol;

main(){

    int x[2], y[2];

    x[0] = 1;
    x[1] = 2;

    y[0] = 1;
    y[1] = 2;

    plot(x,y);

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
