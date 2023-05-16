import ply.lex as lex
import ply.yacc as yacc
import my_lexer
import my_parser
from syntax_test_data import true_positive_tests, true_negative_tests
from symbolTable import SymbolTable

table = SymbolTable()


lexer = lex.lex(module=my_lexer)
parser = yacc.yacc(module=my_parser)

ex = r"""
program my_program;
int global_variable;
int global_variable_looool;

func int sum(int a, float b, char c){
    int i;
}

main(){}
   
"""

result = parser.parse(ex)

print("<-------- SYMBOL TABLE ---------->")
table.print_symbols()
