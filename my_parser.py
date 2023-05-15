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
    """program : PROGRAM ID SEMICOLON var_dec func_opt main"""
    # table.insert(p[2], p[1])


# func_opt
def p_func_opt(p):
    """func_opt : FUNC return_type ID LP param_opt RP func_block func_opt
    | empty"""


# param_opt
def p_param_opt(p):
    """param_opt : type_simple ID more_param_opt
    | empty"""


# more_param_opt
def p_more_param_opt(p):
    """more_param_opt : COMMA type_simple ID more_param_opt
    | empty"""


# var_dec
def p_var_dec(p):
    """var_dec : type_simple ID opt_simple_nodim_assignation opt_dim opt_simple_dim_assignation SEMICOLON var_dec
    | empty"""


# opt_simple_dim_assignation
def p_opt_simple_dim_assignation(p):
    """opt_simple_dim_assignation : EQUAL_ASS LBR INT_NUMBER RBR
    | empty"""


# opt_simple_nodim_assignation
def p_opt_simple_nodim_assignation(p):
    """opt_simple_nodim_assignation : EQUAL_ASS constants
    | empty"""


# opt_dim
def p_opt_dim(p):
    """opt_dim : LSB INT_NUMBER RSB
    | LSB INT_NUMBER RSB LSB INT_NUMBER RSB
    | empty"""


# main
def p_main(p):
    """main : MAIN LP RP func_block"""


# return_type
def p_return_type(p):
    """return_type : type_simple
    | VOID"""


# type_simple
def p_type_simple(p):
    """type_simple : INT_TYPE
    | FLOAT_TYPE
    | CHAR_TYPE"""


# assignation
def p_assignation(p):
    """assignation : var_usage exp_dim_opt EQUAL_ASS exp_or_func_assignation"""


# exp_or_func_assignation
def p_exp_or_func_assignation(p):
    """exp_or_func_assignation : expression_assignation
    | func_call"""


# expression_assignation
def p_expression_assignation(p):
    """expression_assignation : exp SEMICOLON"""


# var_usage
def p_var_usage(p):
    """var_usage : ID exp_dim_opt"""


# exp_dim_opt
def p_exp_dim_opt(p):
    """exp_dim_opt : LSB exp RSB
    | LSB exp RSB LSB exp RSB
    | empty"""


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
    """func_call : ID LP opt_args RP SEMICOLON"""


# opt_args
def p_opt_args(p):
    """opt_args : exp exp_args_more
    | empty"""


# exp_args_more
def p_exp_args_more(p):
    """exp_args_more : COMMA exp exp_args_more
    | empty"""


# statements
def p_statements(p):
    """statements : assignation
    | if_statement
    | while_statement
    | read
    | func_call
    | return
    | print
    | empty"""


def p_print(p):
    """print : PRINT LP opt_string exp RP SEMICOLON"""


def p_opt_string(p):
    """opt_string : empty
    | STRING"""


# block
def p_block(p):
    """block : LBR statements opt_more_statements RBR"""


def p_opt_more_statements(p):
    """opt_more_statements : empty
    | empty_statements"""


def p_empty_statements(p):
    """empty_statements :
    | statements opt_more_statements"""


# func_block
def p_func_block(p):
    """func_block : LBR var_dec statements opt_more_statements RBR"""


# var_usage_opt
def p_var_usage_opt(p):
    """var_usage_opt : var_usage
    | empty"""


# return
def p_return(p):
    """
    return : RETURN LP exp RP SEMICOLON
    """


# method_arg_opt
def p_method_arg_opt(p):
    """
    method_arg_opt : exp meth_exp_more
                   | empty
    """


# method_exp_more
def p_meth_exp_more(p):
    """
    meth_exp_more : COMMA exp meth_exp_more
                  | empty
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
    """


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
