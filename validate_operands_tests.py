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
program my_program;
int a,b,c,d,e,f,g,h;
bool control;

func int uno(int a, int b){

    if(5+10*2 > 5 && 90*(5+3) == 8){}
}

main(){
    int i;
}
   
"""

result = parser.parse(ex)
print()
print("<-------- SYMBOL TABLE ---------->")
table.print_symbols()

print()
print("<-------- Quads ---------->")
quad_list = quads.get_quad_list()
for op, l, r, res in quad_list:
    print(f"{op}, {l}, {r}, {res}")
