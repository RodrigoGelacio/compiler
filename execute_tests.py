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
int i[10];

func int find(int num){

    for(int c=0; c < 10){
        if(i[c] == num){
            return (c);
        }
    }

    return (10);

}

main(){
    int index;

    i[0] = 1;
    i[1] = 2;
    i[2] = 3;
    i[3] = 4;
    i[4] = 5;
    i[5] = 6;
    i[6] = 7;
    i[7] = 8;
    i[8] = 9;
    i[9] = 10;


    index = find(12);

    if(index != 10){
        print(index);
    }
    else{
        print('f');
    }
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
