import ply.lex as lex
import ply.yacc as yacc
import my_lexer
import my_parser
from syntax_test_data import true_positive_tests, true_negative_tests
from symbolTable import SymbolTable
from Quad import Quad
from cubo_semantico import ella_baila_sola

quads = Quad()

table = SymbolTable()


lexer = lex.lex(module=my_lexer)
parser = yacc.yacc(module=my_parser)

ex = r"""
program lol;
int my_int;

main(){

    float f;
    bool boo;

    f = 5 * 2.5;

    if(f > 1){
        f = f + 1;
    }

    print(f);
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
