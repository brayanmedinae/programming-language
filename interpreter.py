from ply.lex import lex
from ply.yacc import yacc

############################################
# Tokenizer
############################################

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


############################################
# Parser
############################################
    
# Define the grammar
def p_expression(p):
    """
    expression  : expression PLUS expression
                | expression REPETITION expression
                | expression MINUS expression
                | expression CONCATENATION expression
    """
    p[0] = (p[2], p[1], p[3])

def p_expression_equal(p):
    """
    expression  : ID EQUAL expression
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
                | STRING
                | ID
    """
    p[0] = p[1]

def p_print(p):
    """
    expression  : PRINT expression
    """
    p[0] = ('print', p[2])

def p_error(p):
    print(f'Syntax error at {p.value!r}')


parser = yacc()

variables = {}

def run(p):
    if type(p) == tuple:
        if p[0] == '+':
            return run(p[1]) + run(p[2])
        elif p[0] == '-':
            return run(p[1]) - run(p[2])
        elif p[0] == '=':
            variables[p[1]] = run(p[2])
            # return variables
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
            # print(run(p[1]))
            return run(p[1])
    else:
        return p


def execute_line(code_line):
    tree = parser.parse(code_line)
    return run(tree)

def get_variables():
    return variables

def get_tokens(code_line):
    lexer.input(code_line)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append({
            'type': tok.type,
            'value': tok.value
        })
    return tokens

def get_tree(code_line):
    return parser.parse(code_line)
