# Pinja Mikkonen 99219
# Priciples of Programming Languages
# Project Work - Phase 4

import sys
import lexer
import syntax
import tree_print
parser = syntax.parser

from semantics_common import visit_tree, SymbolData, SemData
from semantic_checks import semantic_checks, print_symbol_table
from semantics_run import run_program

if __name__ == "__main__":
    import argparse, codecs
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-f', '--file', help='filename to process')

    ns = arg_parser.parse_args()

    if ns.file is None:
        arg_parser.print_help()
    else:
        data = codecs.open( ns.file, encoding='utf-8' ).read()
        ast_tree = parser.parse(data, lexer=lexer.lexer, debug=False)
        tree_print.treeprint(ast_tree) # Just for debugging

        semdata = SemData()
        semantic_checks(ast_tree, semdata)
        print_symbol_table(semdata, "Symbol table:") # Just for debugging
        print("Semantics ok:")
        run_program(ast_tree, semdata)
        print("Program done")

