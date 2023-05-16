import ply.yacc as yacc
import ply.lex as lex
import my_lexer
from my_lexer import tokens
from symbolTable import SymbolTable

table = SymbolTable()


precedence = (
    ("left", "OR"),
    ("left", "AND"),
    ("nonassoc", "EQ", "NE", "GT", "LT", "LE", "GE"),
    ("left", "PLUS", "MINUS"),
    ("left", "MULT", "DIV"),
)


# program
def p_program(p):
    """program : PROGRAM ID SEMICOLON var_dec funcs main"""


# funcs
def p_funcs(p):
    """funcs : FUNC return_type ID change_context_to_func LP params RP func_block funcs
    | empty"""
    if len(p) > 2:
        params = p[6]
        id_name = p[3]
        return_type = p[2]

        table.insert("func", id_name=id_name, return_type=return_type)

        for i in range(0, len(params), 2):
            table.insert("var", id_name=params[i + 1], var_type=params[i])


def p_change_context_to_func(p):
    """change_context_to_func :"""
    table.change_context(p[-1])


# param_opt
def p_params(p):
    """params : type ID more_params
    | empty"""
    if len(p) == 4 and isinstance(p[3], list):
        p[0] = p[1:3] + p[3]
    else:
        p[0] = p[1]


# more_params
def p_more_params(p):
    """more_params : COMMA type ID more_params
    | empty"""
    if len(p) > 2:
        more_params = len(p) - 1
        p[0] = p[2:4] + p[more_params]
    else:
        p[0] = []


# var_dec
def p_var_dec(p):
    """var_dec : type ID dimensionality more_var_decs SEMICOLON var_dec
    | empty"""
    if len(p) > 2:
        var_list = [p[2], p[3]] + p[4]
        var_type = p[1]

        for i in range(0, len(var_list), 2):
            table.insert(
                "var",
                id_name=var_list[i],
                var_type=var_type,
                dimensions=var_list[i + 1],
            )


# dimensionality
def p_dimensionality(p):
    """dimensionality : LSB INT_NUMBER RSB
    | LSB INT_NUMBER RSB LSB INT_NUMBER RSB
    | empty"""
    if len(p) == 4:
        p[0] = [p[2]]
    elif len(p) == 7:
        p[0] = [p[2], p[5]]
    else:
        p[0] = []


# more_var_decs
def p_more_var_decs(p):
    """more_var_decs : COMMA ID dimensionality more_var_decs
    | empty"""
    if len(p) == 5:
        more_var_decs = len(p) - 1
        p[0] = p[more_var_decs] + [p[2], p[3]]
    else:
        p[0] = []


# main
def p_main(p):
    """main : MAIN LP RP func_block"""


# return_type
def p_return_type(p):
    """return_type : type
    | VOID"""
    p[0] = p[1]


# type
def p_type(p):
    """type : INT_TYPE
    | FLOAT_TYPE
    | CHAR_TYPE"""
    p[0] = p[1]


# assignation
def p_assignation(p):
    """assignation : var_usage exp_dim_opt EQUAL_ASS exp SEMICOLON"""


# if_statement
def p_if_statement(p):
    """if_statement : IF LP exp RP block else"""


# else
def p_else(p):
    """else : ELSE block
    | empty"""


# while_statement
def p_while_statement(p):
    """while_statement : WHILE LP exp RP block"""


# read
def p_read(p):
    """read : READ LP var_usage RP SEMICOLON"""


# constants
def p_constants(p):
    """constants : INT_NUMBER
    | FLOAT_NUMBER
    | CHAR"""


# func_call
def p_func_call(p):
    """func_call : ID LP args RP"""


# args
def p_args(p):
    """args : exp more_args
    | empty"""


# more_args
def p_more_args(p):
    """more_args : COMMA exp more_args
    | empty"""


# statements
def p_statements(p):
    """statements : assignation
    | if_statement
    | while_statement
    | read
    | func_call SEMICOLON
    | return
    | print
    | empty"""


def p_print(p):
    """print : PRINT LP string opt_exp RP SEMICOLON"""


def p_opt_exp(p):
    """opt_exp : exp
    | empty"""


def p_string(p):
    """string : empty
    | STRING"""


# block
def p_block(p):
    """block : LBR statements more_statements RBR"""


def p_more_statements(p):
    """more_statements : empty
    | empty_statements"""


def p_empty_statements(p):
    """empty_statements :
    | statements more_statements"""


# func_block
def p_func_block(p):
    """func_block : LBR var_dec statements more_statements RBR"""


# return
def p_return(p):
    """
    return : RETURN LP exp RP SEMICOLON
    """


# arithmetic expression
def p_expression_arithmetic(p):
    """
    exp : exp PLUS exp
        | exp MINUS exp
        | exp MULT exp
        | exp DIV exp
    """


# logical expression
def p_expression_logical(p):
    """
    exp : exp AND exp
        | exp OR exp
    """


# comparative expression
def p_expression_comparator(p):
    """
    exp : exp LT exp
        | exp GT exp
        | exp LE exp
        | exp GE exp
        | exp EQ exp
        | exp NE exp
    """


# base case expression
def p_expression_final(p):
    """
    exp : LP exp RP
        | constants
        | var_usage
        | func_call
    """


# var_usage
def p_var_usage(p):
    """var_usage : ID exp_dim_opt"""


# exp_dim_opt
def p_exp_dim_opt(p):
    """exp_dim_opt : LSB exp RSB
    | LSB exp RSB LSB exp RSB
    | empty"""


# epsilon
def p_empty(p):
    """
    empty :
    """


# Error rule for syntax errors
def p_error(p):
    print("FAIL")
    if p:
        print(f"Syntax error at line {p.lineno}, column {p.lexpos}")
    else:
        print("Syntax error: Unexpected end of file")


# Build lexer
built_lexer = lex.lex(module=my_lexer)

# Build the parser
parser = yacc.yacc()
