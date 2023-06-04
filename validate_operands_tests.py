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
int i[2][2];

func void hola(){
    int j[8][7];

    j[3][1] = 90.8;

    print(j[3][1]);
 
}

main(){

    hola();

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
