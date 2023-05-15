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
    {
        "program": r'''
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
            k = duck(f[k][j], i);
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
    }
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