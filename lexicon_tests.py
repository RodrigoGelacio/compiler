import my_lexer
import ply.lex as lex
from lexic_test_data import lexicons

correct_lexicons=[
    ['ID'], 
    ['ID'], 
    ['ID'], 
    ['IF', 'LP', 'RP', 'LBR', 'RBR'],
    ['ELSE', 'LBR', 'RBR'],
    ['WHILE', 'LP', 'RP'],
    ['ID', 'POINT', 'ID', 'LP','RP']
]

lexer = lex.lex(module=my_lexer)

for i, l in enumerate(lexicons):
    lexer.input(l)
    for j,token in enumerate(lexer):
        assert token.type == correct_lexicons[i][j], f"FAILED, TOKEN NOT CORRECTLY RECOGNIZED. String #{i}, Token #{j}"