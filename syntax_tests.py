import ply.lex as lex
import ply.yacc as yacc
import my_lexer
import my_parser
from syntax_test_data import true_positive_tests, true_negative_tests


lexer = lex.lex(module=my_lexer)
parser = yacc.yacc(module=my_parser)

ex=r'''
program lol;

int i, k, j;
float i[0][0];
int i[0];
int i[0],i[0];

func int sum(){
    int counter;
    int mat[0][0];

    counter = mat[0][0];
    counter = mat[0][1] + sum(50+i[j*7], hola);


    if(7){
        hola();
        hola();
        i = hola();
        if(0){
        
        }
        while(0){
            
        }
    }
    else{
    
    }
}

func void hola(int i){
    print("hello");
}

main(){}
   
'''

result = parser.parse(ex)

print("result:")
print(result)