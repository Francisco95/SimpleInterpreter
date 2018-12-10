import os
from ply import lex, yacc


class MyParser(object):
    """
    Base class for a lexer/parser that has the rules defined as methods.
    Class extracted from PLY examples

    """
    tokens = ()
    precedence = ()

    def __init__(self, **kw):
        """
        constructior for parser lex, can receive a debug parameter

        :param kw: parameters, for now, it receives 'debug'
        """
        self.debug = kw.get('debug', 0)
        self.names = {}
        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[
                1] + "_" + self.__class__.__name__
        except:
            modname = "parser" + "_" + self.__class__.__name__
        self.debugfile = modname + ".dbg"
        self.tabmodule = modname + "_" + "parsetab"
        # print self.debugfile, self.tabmodule

        # Build the lexer and parser
        lex.lex(module=self, debug=self.debug)
        yacc.yacc(module=self,
                  debug=self.debug,
                  debugfile=self.debugfile,
                  tabmodule=self.tabmodule)

    def run(self):
        """
        run the lexer yacc parser by receiving inline inputs

        """
        while 1:
            try:
                s = input('calc > ')
            except EOFError:
                break
            if not s:
                continue
            yacc.parse(s)

    def run_file(self, file_name: str):
        """
        run the lexer yacc parser by receiving a file wih instructions

        :param file_name: the path and name to the file
        """
        pass
