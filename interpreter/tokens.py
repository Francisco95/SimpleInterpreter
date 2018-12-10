from ply import lex, yacc


tokens = (
        'NAME', 'NUMBER',
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
        'LPAREN', 'RPAREN',
        'LBRACE', 'RBRACE',
        'EQ', 'NE', 'GT', 'LT', 'GE', 'LE',
        'SEMI',
    )


# Tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_EQ = r'=='
t_NE = r'!='
t_GT = r'>'
t_LT = r'<'
t_GE = r'>='
t_LE = r'<='
# t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_SEMI = r';'

# ignore tab (\t), space ( ) and newline (\n)
t_ignore = " \t\n"


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %s" % t.value)
        t.value = 0
    # print "parsed number %s" % repr(t.value)
    return t


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = 'NAME'
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    # ('right', 'UMINUS'),
    ('left', 'LT', 'LE', 'GE', 'GT'),
    ('left', 'EQ', 'NE'),
)

lexer = lex.lex()


def p_compute(p):
    """
    compute : expression
            | assign
            | empty
    """
    print(run(p[1]))

def p_assign(p):
    """
    assign : NAME EQUALS expression
    """
    p[0] = ('=', p[1], p[3])


def p_expression(p):
    """
    expression : expression PLUS expression
               | expression MINUS expression
               | expression TIMES expression
               | expression DIVIDE expression
    """
    p[0] = (p[2], p[1], p[3])


def p_expression_number(p):
    """
    expression : NUMBER
    """
    p[0] = p[1]

def p_expression_var(p):
    """
    expression : NAME
    """
    p[0] = ('VAR', p[1])


def p_error(p):
    print("Syntax error found!")

def p_empty(p):
    """
    empty :
    """
    p[0] = None

parser = yacc.yacc()

env = {}
def run(p):
    global env
    if type(p) == tuple:
        if p[0] == '+':
            return run(p[1]) + run(p[2])
        elif p[0] == '-':
            return run(p[1]) - run(p[2])
        elif p[0] == '*':
            return run(p[1]) * run(p[2])
        elif p[0] == '/':
            return run(p[1]) / run(p[2])
        elif p[0] == '=':
            env[p[1]] = run(p[2])
        elif p[0] == 'VAR':
            if p[1] not in env:
                return 'Undeclared variable found!'
            else:
                return env[p[1]]
    else:
        return p

parser.parse("a=100")
# parser.parse("1+a")
while True:
    try:
        s = input('>> ')
    except EOFError:
        break
    parser.parse(s)


# tmp = "a=4;\nb=1;\n c = a-b;"

# lexer.input(tmp)

# while True:
#     tok = lexer.token()
    # if not tok:
    #     break
    # print(tok)
