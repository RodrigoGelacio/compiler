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

    for(int c=3; c < 5){
        print(c);
    }

}
"""

result = parser.parse(ex)
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
