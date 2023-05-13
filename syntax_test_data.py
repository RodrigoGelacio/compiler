true_positive_tests = [
    {
        "program" : r'''
            program lol; main(){}
        '''
    },
    {
        "program" : r'''
            program lol_5; main(){}
        '''
    },
    
]

true_negative_tests = [
    {
        "program" : r'''
            program my_program: main(){}
        '''
    },
]

# {
#         "program":r'''
#             program my_program;
#             class Dog{
#                 attr:
#                     int i;
#                     int j;
#                     float k;
#                 endattr
#                 methods:
#                     func int sum(){
#                         i = 5+5;
#                         return (i);
#                     }
#                 endmeth
#             }
#             func void say_hi(){
#                 print("hola");
#             }
#             main(){
#                 say_hi();
#             }
#         '''
#     }