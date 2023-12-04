from ply.lex import lex
from ply.yacc import yacc

# Tokenizer

reserved = {
    'print': 'PRINT'
}

# All tokens must be named in advance.
tokens = [
    'NUMBER',
    'ID',
    'PLUS',
    'MINUS',
    'EQUAL',
    'CONCATENATION',
    'REPETITION',
    'STRING'
]

tokens += reserved.values()

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'"[a-zA-Z_0-9 ]*"'
    t.value = t.value[1:-1]
    return t

# Token matching rules are written as regexs
t_PLUS = r'\+'
t_MINUS = r'-'
t_EQUAL = r'='
t_CONCATENATION = r'\.'
t_REPETITION = r'\*'

# Ignored characters
t_ignore = ' \t|\n'

# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

# Build the lexer object
lexer = lex()
    
# Parser

# Test it out
data = '''
3 + 4 - 3
a = 3
B = "Hello " . "World"
print B
print "Hello World" * 3
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
# for tok in lexer:
#     print(tok)


# --- Parser
    
# Define the grammar
def p_expression(p):
    """
    expression  : expression PLUS expression
                | expression MINUS expression
                | STRING CONCATENATION STRING
                | ID EQUAL expression
                | ID REPETITION NUMBER
                | ID REPETITION ID
                | NUMBER REPETITION ID
                | NUMBER REPETITION STRING
                | STRING REPETITION NUMBER
    """
    p[0] = (p[2], p[1], p[3])

def p_expression_term(p):
    """
    expression  : term
                | 
    """
    p[0] = p[1]

def p_variable(p):
    """
    expression  : ID
    """
    p[0] = ('id', p[1])

def p_term(p):
    """
    term        : NUMBER
                | ID
                | STRING
    """
    p[0] = p[1]

def p_print(p):
    """
    expression  : PRINT expression
    """
    p[0] = ('print', p[2])

def p_error(p):
    print(f'Syntax error at {p.value!r}')

# Build the parser
parser = yacc()

# Parse an expression
# ast = parser.parse('3 + 4 - 3')
# print(ast)

# ast = parser.parse('"Hello " . "World"')
# print(ast)
variables = {}

def run(p):
    global variables
    if type(p) == tuple:
        if p[0] == '+':
            return run(p[1]) + run(p[2])
        elif p[0] == '-':
            return run(p[1]) - run(p[2])
        elif p[0] == '=':
            variables[p[1]] = run(p[2])
            return variables
        elif p[0] == '.':
            return run(p[1]) + run(p[2])
        elif p[0] == '*':
            return run(p[1]) * run(p[2])
        elif p[0] == 'id':
            if p[1] in variables:
                return variables[p[1]]
            else:
                return 'Undeclared variable'
        elif p[0] == 'print':
            print(run(p[1]))
    else:
        return p
    
while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    result = parser.parse(s)
    print(run(result))


