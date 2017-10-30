import os
import re
import subprocess as sp
import json
import graphviz as gz

from CLexer import CLexer
from CListener import CListener
from CParser import CParser
from antlr4 import *


__all__ = [
    "CAnalysis"
]


class CAnalysisListener(CListener):
    def __init__(self):
        self.defined_functions = []

    def enterFunctionDefinition(self, ctx):
        try:
            n = ctx.declarator().directDeclarator().directDeclarator().getText()
            if n not in self.defined_functions:
                self.defined_functions.append(n)
        except Exception:
            pass


class CAnalysis(object):
    def __init__(self, c_src_file):
        lexer = CLexer(FileStream(c_src_file))
        token_stream = CommonTokenStream(lexer)
        parser = CParser(token_stream)
        tree = parser.compilationUnit()
        walker = ParseTreeWalker()
        self.analysis_listener = CAnalysisListener()
        walker.walk(self.analysis_listener, tree)

    def get_defined_functions(self):
        return self.analysis_listener.defined_functions
