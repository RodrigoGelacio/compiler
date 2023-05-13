var_dec_simple = r'''
    int t[0][8];
    int i, hola;
    float j;
    char j;
    int i = 0;
    int t[0] = {5};
'''

var_dec_complex = r'''
    Dog my_dog;
    Dog my_dog, my_other_dog;
'''

var_dec_opt = r'''
    int t[0][8];
    int i;
    float j;
    char j;
    int i = 0;
    int t[0] = {5};
'''

var_usage = r'''

'''

exp_dim_opt = r'''

'''

exp = r'''
    (5 * 5 + 5 / 5 >= 9) && 0 || 52 / 7 + i
'''
func_call = r'''
    sum(5.5 >= 9 || 0 || 9 || 90 <= 0.89 && 90, 90 + i, 90 || 0, 90.09 + (5-8/90.8) < 0);    
'''

class_opt = r'''
    
'''