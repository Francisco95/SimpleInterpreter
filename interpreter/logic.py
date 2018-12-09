
from interpreter.lexerParser import Parser


class Logic(Parser):

    # define tokens to identify the terminals and non-terminals
    tokens = (
        'NAME', 'NUMBER',
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'NEG', 'EQUALS',  # need to implement NEG
        'LPAREN', 'RPAREN',
        'EQ', 'NE', 'GT', 'LT', 'GE', 'LE',
    )

    # Tokens

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_EQUALS = r'='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_EQ = r'=='
    t_NE = r'!='
    t_GT = r'>'
    t_LT = r'<'
    t_GE = r'>='
    t_LE = r'<='
    t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

    def t_NUMBER(self, t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %s" % t.value)
            t.value = 0
        # print "parsed number %s" % repr(t.value)
        return t

    def t_NEG(self, t):
        try:
            t.value = -int(t.value)
        except ValueError:
            print("Cannot get negative number of %s" % t.value)
            t.value = 0
        return t

    # ignore tab (\t), space (\x20) and newline (\n)
    t_ignore = "\t\x20\n"

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)



