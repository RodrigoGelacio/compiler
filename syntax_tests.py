import ply.lex as lex
import ply.yacc as yacc
import my_lexer
import my_parser
from syntax_test_data import true_positive_tests, true_negative_tests

lexer = lex.lex(module=my_lexer)
parser = yacc.yacc(module=my_parser)

ex=r'''
    program lol; 

    int i = 0;
    float j = 0;

    func int sum(int a, int j, float j){
    
    }
    func int divide(){
        return (i + j);
    }

    main(){
        int i = 0;

        i = sum(0,5,6);

        if (i > 0){
            i = sum(5,5);
            divide();
        }
        else{
            divide();
        }
        if(9+j <= 90){
            while(0){
                if(i && 0){
                    i[0] = j + i;
                    j[0][0] = k+9;
                }
            }
        }

    }
'''

result = parser.parse(ex)

print("result:")
print(result)

# for i, t in enumerate(true_positive_tests):
#     print(f'TP Test#{i+1}:')
#     result = parser.parse(t["program"])
#     print()
    

# for i, t in enumerate(true_negative_tests):
#     print(f'TN Test#{i+1}:')
#     result = parser.parse(t["program"])
#     print()