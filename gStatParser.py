import ply.yacc as yacc
import ply.lex as lex
import gStatLex
from gStatLex import tokens
from symbolTable import SymbolTable
from Quad import Quad
from oracle import ella_baila_sola
from VirtualMachine import VirtualMachine
import math

ind_to_varStr = {0: "int", 1: "float", 2: "char", 3: "bool"}


table = SymbolTable()
quad = Quad()

precedence = (
    ("left", "OR"),
    ("left", "AND"),
    ("nonassoc", "EQ", "NE", "GT", "LT", "LE", "GE"),
    ("left", "PLUS", "MINUS"),
    ("left", "MULT", "DIV"),
)


# program
def p_program(p):
    """program : PROGRAM ID SEMICOLON save_main_quad var_dec funcs main insert_global_size execute"""


def p_execute(p):
    """execute :"""
    VirtualMachine().execute()


def p_save_main_quad(p):
    """save_main_quad :"""
    quad.insert("ERAMAIN", "", "", "main")
    quad.insert("GOTO", "", "", "")
    quad.save_jump()


def p_insert_global_size(p):
    """insert_global_size :"""
    table.insert_global_size()


# funcs
def p_funcs(p):
    """funcs : FUNC return_type ID change_context_to_func insert_parche_guada LP params insert_params RP func_block insert_func_size insert_endproc_quad funcs
    | empty"""

def p_insert_parche_guada(p):
    """insert_parche_guada : """
    if p[-3] != "void":
        table.insert("return", var_type=p[-3])

def p_insert_endproc_quad(p):
    """insert_endproc_quad :"""
    quad.insert("ENDPROC", "", "", "")
    table.reset_local_memory()


def p_insert_func_size(p):
    """insert_func_size :"""
    table.insert_func_size()


def p_insert_params(p):
    """insert_params :"""
    params = p[-1]
    param_types = []
    param_ids = []
    for i in range(0, len(params), 2):
        table.insert("var", id_name=params[i + 1], var_type=params[i])
        param_types.append(params[i])
        param_ids.append(params[i+1])
    table.insert("params", params=param_types)
    table.insert("params_v_addresses", params=param_ids)


def p_change_context_to_func(p):
    """change_context_to_func :"""
    table.change_context(p[-1])
    table.insert("func", id_name=p[-1], return_type=p[-2])


# param_opt
def p_params(p):
    """params : type ID more_params
    | empty"""
    if len(p) == 4 and isinstance(p[3], list):
        p[0] = p[1:3] + p[3]
    else:
        p[0] = []


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
    """var_dec : dim_allowed
    | dim_not_allowed
    | empty"""


def p_dim_not_allowed(p):
    """dim_not_allowed : no_dim_type ID more_var_decs SEMICOLON var_dec
    | empty"""
    if len(p) > 2:
        var_list = [p[2]] + p[3]
        var_type = p[1]

        for i in range(0, len(var_list)):
            if table.is_it_already_declared(var_list[i]):
                raise ValueError(f"{var_list[i]} already declared")
            table.insert(
                "var",
                id_name=var_list[i],
                var_type=var_type,
            )


def p_dim_allowed(p):
    """dim_allowed : dim_type ID dimensionality more_dim_var_decs SEMICOLON var_dec
    | empty"""
    if len(p) > 2:
        var_list = [p[2], p[3]] + p[4]
        var_type = p[1]

        for i in range(0, len(var_list), 2):
            if table.is_it_already_declared(var_list[i]):
                raise ValueError(f"{var_list[i]} already declared")
            if len(var_list[i+1]) == 0:
                table.insert(
                    "var",
                    id_name=var_list[i],
                    var_type=var_type,
                )
            else:
                table.insert(
                    "var",
                    id_name=var_list[i],
                    dim = True,
                    var_type=var_type,
                    dimensions = var_list[i+1]
                )


def p_more_dim_var_decs(p):
    """more_dim_var_decs : COMMA ID dimensionality more_dim_var_decs
    | empty"""
    if len(p) == 5:
        more_var_decs = len(p) - 1
        p[0] = p[more_var_decs] + [p[2], p[3]]
    else:
        p[0] = []


def p_dim_type(p):
    """dim_type : FLOAT_TYPE
    | INT_TYPE"""
    p[0] = p[1]


def p_no_dim_type(p):
    """no_dim_type : BOOL_TYPE
    | CHAR_TYPE"""
    p[0] = p[1]


# dimensionality
def p_dimensionality(p):
    """dimensionality : LSB INT_NUMBER RSB
    | LSB INT_NUMBER RSB LSB INT_NUMBER RSB
    | empty"""
    if len(p) == 4:
        table.insert("constant", id_name=0)
        table.insert("constant", id_name=p[2])
        p[0] = [p[2]]
    elif len(p) == 7:
        table.insert("constant", id_name=0)
        table.insert("constant", id_name=p[2])
        table.insert("constant", id_name=p[5])
        p[0] = [p[2], p[5]]
    else:
        p[0] = []


# more_var_decs
def p_more_var_decs(p):
    """more_var_decs : COMMA ID more_var_decs
    | empty"""
    if len(p) == 4:
        more_var_decs = len(p) - 1
        p[0] = p[more_var_decs] + [p[2]]
    else:
        p[0] = []


# main
def p_main(p):
    """main : MAIN update_goto_main_quad change_context_to_main LP RP func_block insert_func_size insert_endproc_main"""

def p_insert_endproc_main(p):
    """insert_endproc_main : """
    quad.insert("ENDPROCMAIN","","","")

def p_update_goto_main_quad(p):
    """update_goto_main_quad :"""
    curr_quad = quad.get_current_quad_index()
    quad.insert_direction_to_quad(curr_quad)


def p_change_context_to_main(p):
    """change_context_to_main :"""
    table.change_context("main")


# return_type
def p_return_type(p):
    """return_type : type
    | VOID"""
    p[0] = p[1]


# type
def p_type(p):
    """type : INT_TYPE
    | FLOAT_TYPE
    | CHAR_TYPE
    | BOOL_TYPE"""
    p[0] = p[1]


# assignation
def p_assignation(p):
    """assignation : var_usage EQUAL_ASS exp SEMICOLON"""
    identifier = p[1]
    expression = p[3]

    id_assignee, var_type_assignee, v_address_assignee = table.validate(identifier)
    id_expression, var_type_expression, v_address_expression = table.validate(
        expression
    )

    if ella_baila_sola(var_type_assignee, var_type_expression, "=") == -1:
        raise ValueError(
            f"Incompatible types {var_type_assignee} and {var_type_expression} with = operator"
        )

    quad.insert("=", v_address_expression, "", v_address_assignee)


# if_statement
def p_if_statement(p):
    """if_statement : IF LP exp insert_go_to_false RP block insert_go_to else"""


def p_insert_go_to_false(p):
    """insert_go_to_false :"""
    expression = p[-1]
    _, _, v_add = table.validate(expression)
    quad.insert("GOTOF", v_add, "", "")
    quad.save_jump()


def p_insert_go_to(p):
    """insert_go_to :"""
    quad.insert("GOTO", "", "", "")
    curr_quad_index = quad.get_current_quad_index()
    quad.insert_direction_to_quad(curr_quad_index)
    quad.save_jump()


# else
def p_else(p):
    """else : ELSE block
    | empty"""

    curr_quad_index = quad.get_current_quad_index()

    quad.insert_direction_to_quad(curr_quad_index)


# while_statement
def p_while_statement(p):
    """while_statement : WHILE LP save_exp_start_direction exp insert_go_to_false RP block insert_go_to_while"""


def p_insert_go_to_while(p):
    """insert_go_to_while :"""
    pending_jump = quad.get_go_to_direction_while_statement()
    quad.insert("GOTO", "", "", pending_jump)
    curr_quad_dir = quad.get_current_quad_index()
    quad.insert_direction_to_quad(curr_quad_dir)


def p_save_exp_start_direction(p):
    """save_exp_start_direction :"""
    quad.save_start_exp_direction()


# read
def p_read(p):
    """read : READ LP var_usage RP SEMICOLON"""

    _,_,v_add= table.validate(p[3])

    quad.insert("READ", "", "", v_add)


# constants
def p_constants(p):
    """constants : INT_NUMBER
    | FLOAT_NUMBER
    | CHAR
    | BOOL"""

    table.insert("constant", id_name=p[1])
    if isinstance(p[1], bool):
        p[0] = str(p[1])
    else:
        p[0] = p[1]


# func_call
def p_func_call(p):
    """func_call : ID make_ERA_quad LP args RP"""
    func_name = p[1]
    args = p[4]

    if not table.func_exists(func_name):
        raise ValueError(f"Function {func_name} is not declared.")
    
    arg_ids, v_address = table.validate_args(func_name, args)

    for i, v_add in enumerate(v_address):
        v_add_param =table.get_param_v_add(func_name, i)
        quad.insert("PARAM", v_add, "", v_add_param)
    
    init_func_quad = table.get_func_quad(func_name)
    # GOSUB quadruple
    quad.insert("GOSUB", "", "", init_func_quad)

    return_func_type = table.get_return_type_func(func_name)

    if return_func_type != "void":

        var_type = table.validate_return_function(func_name)

        temp = "t" + str(table.get_current_temp())
        table.insert(
            "temp",
            id_name=temp,
            var_type=var_type,
        )

        _, _, v_address = table.validate((temp, 0))
        func_var_v_address = table.get_func_var_v_address(func_name)
        quad.insert("=", func_var_v_address, "", v_address)

        p[0] = (temp, 0)


def p_make_ERA_quad(p):
    """make_ERA_quad  :"""
    quad.insert("ERA", "", "", p[-1])


# args
def p_args(p):
    """args : exp more_args
    | empty"""

    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


# more_args
def p_more_args(p):
    """more_args : COMMA exp more_args
    | empty"""
    if len(p) == 4:
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []


# statements
def p_statements(p):
    """statements : assignation
    | if_statement
    | while_statement
    | for_loop
    | read
    | func_call SEMICOLON
    | return
    | print
    | plot
    | empty"""

    p[0] = p[1]

def p_for_loop(p):
    """for_loop : FOR LP for_var_dec save_exp_start_direction SEMICOLON exp insert_go_to_false RP block add_one_to_control insert_go_to_while"""

def p_for_var_dec(p):
    """for_var_dec : INT_TYPE ID EQUAL_ASS INT_NUMBER """

    var_type = p[1]
    var_id = p[2]
    const = p[4]

    if table.is_it_already_declared(var_id):
        raise ValueError(f"{var_id} already declared")

    table.insert("var", id_name=var_id, var_type=var_type)
    table.insert("constant", id_name=const)

    const_v_add = table.get_virtual_add_const(const)
    _,_,var_v_add = table.validate((var_id, "_"))

    quad.insert("=",const_v_add,"",var_v_add)

    p[0] = var_id

def p_add_one_to_control(p):
    """add_one_to_control : """
    table.insert("constant", id_name=1)
    _,_,control_var_v_add = table.validate((p[-7], "_"))
    one_v_add = table.get_virtual_add_const(1)

    quad.insert("+", one_v_add, control_var_v_add, control_var_v_add)


def p_print(p):
    """print : PRINT LP print_args RP SEMICOLON"""

    if p[3] != None:
        _, _, v_address = table.validate(p[3])
        quad.insert("PRINT", "", "", v_address)
    
    else:
        quad.insert("PRINT", "", "", -1)


def p_print_args(p):
    """print_args : string_or_exp
    | empty"""
    p[0] = p[1]


def p_exp_print(p):
    """string_or_exp : exp"""
    p[0] = p[1]


def p_string_print(p):
    """string_or_exp : STRING"""
    p[0] = p[1]


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
    """func_block : LBR var_dec save_init_func statements more_statements RBR"""


def p_save_init_func(p):
    """save_init_func :"""
    curr_quead_ind = quad.get_current_quad_index()
    table.insert_quad_index_where_func_starts(curr_quead_ind)


# return
def p_return(p):
    """
    return : RETURN LP exp RP SEMICOLON
    """
    exp = p[3]
    table.is_return_type_ok(exp)
    _, _, v_address = table.validate(exp)
    func_name = table.get_current_context()
    func_var_v_address = table.get_func_var_v_address(func_name)
    quad.insert("RETURN", func_var_v_address, "", v_address)


# arithmetic expression
def p_expression_arithmetic(p):
    """
    exp : exp PLUS exp
        | exp MINUS exp
        | exp MULT exp
        | exp DIV exp
        | exp LT exp
        | exp GT exp
        | exp LE exp
        | exp GE exp
        | exp EQ exp
        | exp NE exp
        | exp AND exp
        | exp OR exp
    """
    left_op = p[1]
    right_op = p[3]
    operation = p[2]

    left_op, type_left_operand, left_op_v_add = table.validate(left_op)
    right_op, type_right_operand, right_op_v_add = table.validate(right_op)

    ind_var_type = ella_baila_sola(type_left_operand, type_right_operand, operation)
    if ind_var_type == -1:
        raise ValueError(
            f"{type_left_operand} is not compatible with {type_right_operand} with {operation}."
        )
    else:
        temp = "t" + str(table.get_current_temp())
        table.insert(
            "temp",
            id_name=temp,
            var_type=ind_to_varStr[ind_var_type],
        )
        _, _, temp_v_add = table.validate((temp, 0))
        quad.insert(operation, left_op_v_add, right_op_v_add, temp_v_add)

        p[0] = (temp, 0)


# base case expression
def p_expression_final(p):
    """
    exp : LP exp RP
        | constants
        | var_usage
        | func_call
    """
    if len(p) > 2:
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_plot(p):
    """plot : PLOT LP ID COMMA ID RP SEMICOLON"""

    x_id,_,x_v_add = table.validate((p[3], "_"))
    y_id,_,y_v_add = table.validate((p[5], "_"))

    _,x_dims,_ = table.get_dim_var_info(x_id)
    _,y_dims,_ = table.get_dim_var_info(y_id)

    if len(x_dims) == 1 and len(y_dims) == 1:
        x_size = math.prod(x_dims)
        y_size = math.prod(y_dims)

        quad.insert("PLOT",(x_v_add, x_size), (y_v_add, y_size), "")

    else:
        raise Exception("Plot function only works with unidimensional arrays")


# var_usage
def p_var_usage(p):
    """var_usage : ID exp_dim_opt"""
    if len(p[2]) != 0:
        p[0] = p[2]
    else:
        p[0] = (p[1], "_")


# exp_dim_opt
def p_exp_dim_opt(p):
    """exp_dim_opt : LSB exp RSB
    | LSB exp RSB LSB exp RSB
    | empty"""
    if len(p) == 4:
        # get initial v_add of dim variable and its dimensions
        base_v_add, dims, var_type = table.get_dim_var_info(p[-1])

        if len(dims) != 1:
            raise Exception(f"Wrong dimensional access on '{p[-1]}'")

        # get v_add of upper_boundary and lower_boundary(0) of dim
        _, _, upper_dim_v_add = table.validate(dims[0])
        _, _, lower_dim_v_add = table.validate(0)

        # validate the argument exists and get its v_add
        _, _, index_v_add = table.validate(p[2])

        # insert quad to verify at run time the exp is within bounds
        quad.insert("VER", index_v_add, lower_dim_v_add, upper_dim_v_add)

        # add bas_v_add to constants
        table.insert("constant", id_name=base_v_add)

        # get v_add of base_v_add
        _, _, ptr_to_base_v_add = table.validate(base_v_add)

        # insert ptr to symbol table, ptr will be pointing towards the direction of the casilla
        ptr = "pt" + str(table.get_current_ptr())
        table.insert("pointer", id_name=ptr, var_type=var_type)

        # get v_add of pointer that pointing towards the casilla
        casilla_ptr = table.get_ptr_v_add(ptr)

        quad.insert("+s", index_v_add, ptr_to_base_v_add, casilla_ptr)

        p[0] = (ptr, "ptr")
    elif len(p) > 4:
        # info of dim variable
        base_v_add, dims, var_type = table.get_dim_var_info(p[-1])

        if len(dims) != 2:
            raise Exception(f"Wrong dimensional access on '{p[-1]}'")

        # get v_add of upper_boundary and lower_boundary(0) of dims for first dim
        _, _, upper_dim_v_add_1 = table.validate(dims[0])
        _, _, lower_dim_v_add_1 = table.validate(0)

        # get v_add of upper_boundary and lower_boundary(0) of dims for second dim
        _, _, upper_dim_v_add_2 = table.validate(dims[1])
        lower_dim_v_add_2 = lower_dim_v_add_1

        # info of expressions
        _, _, index_v_add_1 = table.validate(p[2])
        _, _, index_v_add_2 = table.validate(p[5])

        # insert quad verification
        quad.insert("VER", index_v_add_1, lower_dim_v_add_1, upper_dim_v_add_1)
        quad.insert("VER", index_v_add_2, lower_dim_v_add_2, upper_dim_v_add_2)

        # add base_v_add to constants
        table.insert("constant", id_name=base_v_add)

        # get v_add of base address
        _, _, ptr_to_base_v_add = table.validate(base_v_add)

        # create new temp and get its v_address
        temp = "t" + str(table.get_current_temp())
        table.insert("temp", id_name=temp, var_type=var_type)
        _, _, temp_v_add = table.validate((temp, 0))

        # quad to jump number of rows
        quad.insert("*", index_v_add_1, upper_dim_v_add_2, temp_v_add)

        # create new temp and get its v_address
        temp = "t" + str(table.get_current_temp())
        table.insert("temp", id_name=temp, var_type=var_type)
        _, _, temp_v_add_2 = table.validate((temp, 0))

        # quad to add the number of cols
        quad.insert("+", index_v_add_2, temp_v_add, temp_v_add_2)

        # create ptr that points to the casilla and get its v_add
        ptr = "pt" + str(table.get_current_ptr())
        table.insert("pointer", id_name=ptr, var_type=var_type)
        ptr_to_casilla = table.get_ptr_v_add(ptr)

        # quad that saves the v_add of the casilla to the pointer prev created
        quad.insert("+s", temp_v_add_2, ptr_to_base_v_add, ptr_to_casilla)

        # return ptr
        p[0] = (ptr, "ptr")

    else:
        p[0] = []


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
built_lexer = lex.lex(module=gStatLex)

# Build the parser
parser = yacc.yacc()
