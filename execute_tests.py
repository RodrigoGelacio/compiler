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

func int fibonacciR(int num){
    if(num == 0){
        return (0);
    }
    if(num == 1){
        return (1);
    }

    return (fibonacciR(num-1)+fibonacciR(num-2));
}

func int fibonacciI(int n){
    int num1, num2, num3;

    num1 = 0;
    num2 = 1;

    for(int c=0; c < n){
        num3 = num1 + num2;
        num1 = num2;
        num2 = num3;
    }

    return (num1);
}

main(){

    int i;

    i = fibonacciR(20);

    print(i);

    i = fibonacciI(20);

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
