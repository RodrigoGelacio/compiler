import ply.lex as lex

reserved = {
    "program": "PROGRAM",
    "main": "MAIN",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "func": "FUNC",
    "return": "RETURN",
    "read": "READ",
    "print": "PRINT",
    "void": "VOID",
    "int": "INT_TYPE",
    "float": "FLOAT_TYPE",
    "char": "CHAR_TYPE",
}

tokens = [
    "LSB",
    "RSB",
    "LP",
    "RP",
    "LBR",
    "RBR",
    "COMMA",
    "SEMICOLON",
    "INT_NUMBER",
    "FLOAT_NUMBER",
    "ID",
    "AND",
    "OR",
    "GT",
    "LE",
    "GE",
    "LT",
    "EQ",
    "NE",
    "EQUAL_ASS",
    "PLUS",
    "MINUS",
    "MULT",
    "DIV",
    "STRING",
    "CHAR",
]

tokens = tokens + list(reserved.values())

# Regular expressions for tokens
t_LSB = r"\["
t_RSB = r"\]"
t_LP = r"\("
t_RP = r"\)"
t_LBR = r"\{"
t_RBR = r"\}"
t_COMMA = r","
t_SEMICOLON = r";"
t_INT_NUMBER = r"\d+"
t_FLOAT_NUMBER = r"[-+]?(\d+(\.\d+))([eE][-+]?\d+)?"
t_AND = r"&&"
t_OR = r"\|\|"
t_GT = r">"
t_LT = r"<"
t_EQ = r"=="
t_NE = r"!="
t_LE = r"<="
t_GE = r">="
t_EQUAL_ASS = r"="
t_PLUS = r"\+"
t_MINUS = r"-"
t_MULT = r"\*"
t_DIV = r"\/"
t_STRING = r'".*"'
t_CHAR = r"'.'"

# Ignored characters (spaces and tabs)
t_ignore = " \t"


# Define a rule to handle newlines
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


# ID tokens and reserved words lookup
def t_ID(t):
    r"[a-zA-Z_]\w*"
    t.type = reserved.get(t.value, "ID")
    return t


# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)
