
from interpreter.lexerParser import MyParser, yacc, lex


class Logic(MyParser):

    # define tokens to identify the terminals and non-terminals
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
    t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

    t_SEMI = r';'

    def t_NUMBER(self, t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %s" % t.value)
            t.value = 0
        # print "parsed number %s" % repr(t.value)
        return t

    # ignore tab (\t), space ( ) and newline (\n)
    t_ignore = " \t\n"

    def t_newline(self, t):
        r';+'
        t.lexer.lineno += t.value.count(";")

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

        # Parsing rules
    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'UMINUS'),
    )

    def p_statement_assign(self, p):
        'statement : NAME EQUALS expression'
        self.names[p[1]] = p[3]

    def p_statement_expr(self, p):
        'statement : expression'
        print(p[1])

    def p_expression_binop(self, p):
        """
        expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression EQ expression
                  | expression NE expression
                  | expression GT expression
                  | expression LT expression
                  | expression GE expression
                  | expression LE expression
        """
        # print [repr(p[i]) for i in range(0,4)]
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]
        elif p[2] == '==':
            p[0] = p[1] == p[2]
        elif p[2] == '!=':
            p[0] = p[1] != p[2]
        elif p[2] == '>':
            p[0] = p[1] > p[2]
        elif p[2] == '<':
            p[0] = p[1] < p[2]
        elif p[2] == '>=':
            p[0] = p[1] >= p[2]
        elif p[2] == '<=':
            p[0] = p[1] <= p[2]

    def p_expression_uminus(self, p):
        'expression : MINUS expression %prec UMINUS'
        p[0] = -p[2]

    def p_expression_group(self, p):
        'expression : LPAREN expression RPAREN'
        p[0] = p[2]

    def p_expression_block(self, p):
        'expression : LBRACE expression RBRACE'
        p[0] = p[2]

    def p_expression_number(self, p):
        'expression : NUMBER'
        p[0] = p[1]

    def p_expression_name(self, p):
        'expression : NAME'
        try:
            p[0] = self.names[p[1]]
        except LookupError:
            print("Undefined name '%s'" % p[1])
            p[0] = 0

    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")


if __name__ == '__main__':
    l = Logic()
    tmp = "a=4\nb=1\n c = a-b"
    lexer = lex.lex()
    lexer.input(tmp)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
    # yacc.parse(tmp)
    # print(tmp)
    # for c in list(tmp):
    #     yacc.parse(c)
    # l.run()
