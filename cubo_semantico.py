from collections import defaultdict

"""
INT =       0
FLOAT =     1
CHAR =      2
BOOL =      3
ERROR =    -1
"""


def ella_baila_sola(op1_var_type, op2_var_type, operation):
    """Oraculo nos dice si los dos operandos pueden bailar.

    Args:
        op1: str "int", "float", "char", "bool"
        op2: str "int", "float", "char", "bool"
        op3: str "+", "-", "/", "*"

    Returns:
        bool: True si los tipos no son compatibles :(, false en el otro caso.
    """

    if isinstance(op1_var_type, str) and op1_var_type[0] != "'":
        ind_op_1 = ind_with_var(op1_var_type)
    else:
        ind_op_1 = ind_with_const(op1_var_type)

    if isinstance(op2_var_type, str) and op2_var_type[0] != "'":
        ind_op_2 = ind_with_var(op2_var_type)
    else:
        ind_op_2 = ind_with_const(op2_var_type)

    if ind_op_1 != -1 and ind_op_2 != -1:
        return cubo[ind_op_1][ind_op_2][operation]

    else:
        raise ValueError("El operante no es compatible con los tipos de este lenguaje.")


def ind_with_var(op):

    var_to_ind = {"int": 0, "float": 1, "char": 2, "bool": 3}

    return var_to_ind[op]


def ind_with_const(op):
    if isinstance(op, bool):
        return 3
    elif isinstance(op, int):
        return 0
    elif isinstance(op, float):
        return 1
    elif isinstance(op, str):
        return 2
    else:
        return -1


cubo = {}
cubo[0] = {}
cubo[0][0] = {}
cubo[0][1] = {}
cubo[0][2] = {}
cubo[0][3] = {}

cubo[0][0]["+"] = 0
cubo[0][0]["-"] = 0
cubo[0][0]["*"] = 0
cubo[0][0]["/"] = 0
cubo[0][0]["&&"] = -1
cubo[0][0]["||"] = -1
cubo[0][0][">"] = 3
cubo[0][0]["<"] = 3
cubo[0][0][">="] = 3
cubo[0][0]["<="] = 3
cubo[0][0]["=="] = 3
cubo[0][0]["=="] = 3
cubo[0][0]["="] = 0

cubo[0][1]["+"] = 1
cubo[0][1]["-"] = 1
cubo[0][1]["*"] = 1
cubo[0][1]["/"] = 1
cubo[0][1]["&&"] = -1
cubo[0][1]["||"] = -1
cubo[0][1][">"] = 3
cubo[0][1]["<"] = 3
cubo[0][1][">="] = 3
cubo[0][1]["<="] = 3
cubo[0][1]["=="] = 3
cubo[0][1]["="] = 1

cubo[0][2]["+"] = -1
cubo[0][2]["-"] = -1
cubo[0][2]["*"] = -1
cubo[0][2]["/"] = -1
cubo[0][2]["&&"] = -1
cubo[0][2]["||"] = -1
cubo[0][2][">"] = -1
cubo[0][2]["<"] = -1
cubo[0][2][">="] = -1
cubo[0][2]["<="] = -1
cubo[0][2]["=="] = -1
cubo[0][2]["="] = -1

cubo[0][3]["+"] = -1
cubo[0][3]["-"] = -1
cubo[0][3]["*"] = -1
cubo[0][3]["/"] = -1
cubo[0][3]["&&"] = -1
cubo[0][3]["||"] = -1
cubo[0][3][">"] = -1
cubo[0][3]["<"] = -1
cubo[0][3][">="] = -1
cubo[0][3]["<="] = -1
cubo[0][3]["=="] = -1
cubo[0][3]["="] = -1

cubo[1] = {}
cubo[1][0] = {}
cubo[1][1] = {}
cubo[1][2] = {}
cubo[1][3] = {}

cubo[1][0]["+"] = 1
cubo[1][0]["-"] = 1
cubo[1][0]["*"] = 1
cubo[1][0]["/"] = 1
cubo[1][0]["&&"] = -1
cubo[1][0]["||"] = -1
cubo[1][0][">"] = 3
cubo[1][0]["<"] = 3
cubo[1][0][">="] = 3
cubo[1][0]["<="] = 3
cubo[1][0]["=="] = 3
cubo[1][0]["="] = 1

cubo[1][1]["+"] = 1
cubo[1][1]["-"] = 1
cubo[1][1]["*"] = 1
cubo[1][1]["/"] = 1
cubo[1][1]["="] = 1
cubo[1][1]["&&"] = -1
cubo[1][1]["||"] = -1
cubo[1][1][">"] = 3
cubo[1][1]["<"] = 3
cubo[1][1][">="] = 3
cubo[1][1]["<="] = 3
cubo[1][1]["=="] = 3

cubo[1][2]["+"] = -1
cubo[1][2]["-"] = -1
cubo[1][2]["*"] = -1
cubo[1][2]["/"] = -1
cubo[1][2]["="] = -1
cubo[1][2]["&&"] = -1
cubo[1][2]["||"] = -1
cubo[1][2][">"] = -1
cubo[1][2]["<"] = -1
cubo[1][2][">="] = -1
cubo[1][2]["<="] = -1
cubo[1][2]["=="] = -1

cubo[1][3]["+"] = -1
cubo[1][3]["-"] = -1
cubo[1][3]["*"] = -1
cubo[1][3]["/"] = -1
cubo[1][3]["="] = -1
cubo[1][3]["&&"] = -1
cubo[1][3]["||"] = -1
cubo[1][3][">"] = -1
cubo[1][3]["<"] = -1
cubo[1][3][">="] = -1
cubo[1][3]["<="] = -1
cubo[1][3]["=="] = -1

cubo[2] = {}
cubo[2][0] = {}
cubo[2][1] = {}
cubo[2][2] = {}
cubo[2][3] = {}

cubo[2][0]["+"] = -1
cubo[2][0]["-"] = -1
cubo[2][0]["*"] = -1
cubo[2][0]["/"] = -1
cubo[2][0]["="] = -1
cubo[2][0]["&&"] = -1
cubo[2][0]["||"] = -1
cubo[2][0][">"] = -1
cubo[2][0]["<"] = -1
cubo[2][0][">="] = -1
cubo[2][0]["<="] = -1
cubo[2][0]["=="] = -1

cubo[2][1]["+"] = -1
cubo[2][1]["-"] = -1
cubo[2][1]["*"] = -1
cubo[2][1]["/"] = -1
cubo[2][1]["="] = -1
cubo[2][1]["&&"] = -1
cubo[2][1]["||"] = -1
cubo[2][1][">"] = -1
cubo[2][1]["<"] = -1
cubo[2][1][">="] = -1
cubo[2][1]["<="] = -1
cubo[2][1]["=="] = -1

cubo[2][2]["+"] = -1
cubo[2][2]["-"] = -1
cubo[2][2]["*"] = -1
cubo[2][2]["/"] = -1
cubo[2][2]["="] = -1
cubo[2][2]["&&"] = -1
cubo[2][2]["||"] = -1
cubo[2][2][">"] = -1
cubo[2][2]["<"] = -1
cubo[2][2][">="] = -1
cubo[2][2]["<="] = -1
cubo[2][2]["=="] = 3

cubo[2][3]["+"] = -1
cubo[2][3]["-"] = -1
cubo[2][3]["*"] = -1
cubo[2][3]["/"] = -1
cubo[2][3]["="] = -1
cubo[2][3]["&&"] = -1
cubo[2][3]["||"] = -1
cubo[2][3][">"] = -1
cubo[2][3]["<"] = -1
cubo[2][3][">="] = -1
cubo[2][3]["<="] = -1
cubo[2][3]["=="] = -1

cubo[3] = {}
cubo[3][0] = {}
cubo[3][1] = {}
cubo[3][2] = {}
cubo[3][3] = {}

cubo[3][0]["+"] = -1
cubo[3][0]["-"] = -1
cubo[3][0]["*"] = -1
cubo[3][0]["/"] = -1
cubo[3][0]["="] = -1
cubo[3][0]["&&"] = -1
cubo[3][0]["||"] = -1
cubo[3][0][">"] = -1
cubo[3][0]["<"] = -1
cubo[3][0][">="] = -1
cubo[3][0]["<="] = -1
cubo[3][0]["=="] = -1

cubo[3][1]["+"] = -1
cubo[3][1]["-"] = -1
cubo[3][1]["*"] = -1
cubo[3][1]["/"] = -1
cubo[3][1]["="] = -1
cubo[3][1]["&&"] = -1
cubo[3][1]["||"] = -1
cubo[3][1][">"] = -1
cubo[3][1]["<"] = -1
cubo[3][1][">="] = -1
cubo[3][1]["<="] = -1
cubo[3][1]["=="] = -1

cubo[3][2]["+"] = -1
cubo[3][2]["-"] = -1
cubo[3][2]["*"] = -1
cubo[3][2]["/"] = -1
cubo[3][2]["="] = -1
cubo[3][2]["&&"] = -1
cubo[3][2]["||"] = -1
cubo[3][2][">"] = -1
cubo[3][2]["<"] = -1
cubo[3][2][">="] = -1
cubo[3][2]["<="] = -1
cubo[3][2]["=="] = -1

cubo[3][3]["+"] = -1
cubo[3][3]["-"] = -1
cubo[3][3]["*"] = -1
cubo[3][3]["/"] = -1
cubo[3][3]["="] = 3
cubo[3][3]["&&"] = 3
cubo[3][3]["||"] = 3
cubo[3][3][">"] = -1
cubo[3][3]["<"] = -1
cubo[3][3][">="] = -1
cubo[3][3]["<="] = -1
cubo[3][3]["=="] = 3
