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
int i,j,k;
float f;

func void uno(int a, int b){
    if(a>0){
        i = a + b * j + i;
        print(i+j);
        uno(a-i, i);
    }
    else{
        print(a + b);
    }
}


func int dos(int a, float g){

    i = a;

    print('a');

    while(a>0){
        a = a - k * j;
        uno(a*2, a+k);
        g = g*j-k;
    }

    return (i+k*j);
}

main(){
    int my_int;
    float my_float;
    i = 2;
    k = i + 1;
    f = 3.14 + dos(my_int, my_float);
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
