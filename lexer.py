from ply import lex

tokens = [
    'LSB',
    'RSB',
    'LP',
    'RP',
    'LBR',
    'RBR',
    'COMMA',
    'SEMICOLON',
    'COLON',
    'INT',
    'FLOAT',
    'ID',
    'AND',
    'OR',
    'GT',
    'LT',
    'EQ',
    'NEQ',
    'EQUAL_ASS',
    'PLUS',
    'MINUS',
    'MULT',
    'DIV',
    'POINT',
    'STRING',
    'CHAR',
    'PROGRAM',
    'CLASS',
    'MAIN',
    'IF',
    'ELSE',
    'WHILE',
    'FUNC',
    'RETURN',
    'READ',
    'PRINT',
    'VOID',
    'ATTR',
    'ENDATTR',
    'METHODS',
    'ENDMETH',
]

# Regular expression rules for tokens
t_LSB = r'\['
t_RSB = r'\]'
t_LP = r'\('
t_RP = r'\)'
t_LBR = r'\{'
t_RBR = r'\}'
t_COMMA = r','
t_SEMICOLON = r';'
t_COLON = r':'
t_INT = r'^\d+$'
t_FLOAT = r'[-+]?(\d+(\.\d+))([eE][-+]?\d+)?'
t_ID = r'[a-zA-Z_]\w*'
t_AND = r'&&'
t_OR = r'\|\|'
t_GT = r'>'
t_LT = r'<'
t_EQ = r'=='
t_NEQ = r'!='
t_EQUAL_ASS = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'\/'
t_POINT = r'\.'
t_STRING = r'".*"'
t_CHAR = r"'.'"
t_PROGRAM = r'program'
t_CLASS = r'class'
t_MAIN = r'main'
t_IF = r'if'
t_ELSE = r'else'
t_WHILE = r'while'
t_FUNC = r'func'
t_RETURN = r'return'
t_READ = r'read'
t_PRINT = r'print'
t_VOID = r'void'
t_ATTR = r'attr'
t_ENDATTR = r'endattr'
t_METHODS = r'methods'
t_ENDMETH = r'endmeth'

# Ignored characters (spaces and tabs)
t_ignore = ' \t'

# Define a rule to handle newlines
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
