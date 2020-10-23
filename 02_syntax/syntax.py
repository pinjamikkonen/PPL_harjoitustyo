import ply.yacc as yacc
import lexer.py as lexer

from lexer import tokens

def p_program(p):
    'program: {function_or_variable_definition} statement_list'
    print('program')

def p_function_or_variable_definition(p):
    'function_or_variable_definition: variable_definition | function_definition | subroutine_definition'

def p_variable_definition(p):


def p_function_call(p):
    'function_call: FUNC_IDENT LSQUARE [arguments] RSQUARE'
    print('function call')

def p_error(p):
    print("Jokin meni vitusti pieleen!")

parser = yacc.yacc()

if __name__ == '__main__':
    import argparse, codecs
    arg_parser = argparse.ArgumentParser()
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this' )
    group.add_argument('-f', '--file', help='filename to process')
    ns = arg_parser.parse_args()
    if ns.who == True:
        # identify who wrote this
        print( '99219 Pinja Mikkonen :)' )
    elif ns.file is None:
        # user didn't provide input filename
        arg_parser.print_help()
    else:
        data = codecs.open( ns.file, encoding='utf-8' ).read()
        result = parser.parse(data, lexer=lexer.lexer, debug=False)
        if result is None:
            print( 'syntax OK' )
