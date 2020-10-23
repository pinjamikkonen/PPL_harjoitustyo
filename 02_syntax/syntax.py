# Pinja Mikkonen 99219
# Priciples of Programming Languages
# Project Work - Phase 2

import ply.yacc as yacc
import lexer.py as lexer

from lexer import tokens

def p_program(p):
    'program: {function_or_variable_definition} statement_list'
    print('program')

def p_function_or_variable_definition(p):
    '''function_or_variable_definition: variable_definition
                                        | function_definition
                                        | subroutine_definition'''
    print('function_or_variable_definition')

def p_variable_definition(p):
    '''variable_definition: scalar_definition
                            | range_definition
                            | sheet_definition'''
    print('variable_definition')

def p_function_definition(p):
    '''function_definition: FUNCTION FUNC_IDENT LSQUARE [formals] RSQUARE
                            RETURN (SCALAR | RANGE) IS
                            {variable_definition}
                            statement_list
                            END'''
    print('function_definition')

def p_subroutine_definition(p):
    '''subroutine_definition:   SUBROUTINE FUNC_IDENT LSQUARE [formals] RSQUARE IS
                                {variable_definition}
                                statement_list
                                END'''
    print('subroutine_definition')

def p_formals(p):
    'formals: formal_arg {COMMA formal_arg}'
    print('formals')

def p_formal_arg(p):
     '''formal_arg: IDENT COLON SCALAR
                    | RANGE_IDENT COLON RANGE
                    | SHEET_IDENT COLON SHEET'''
     print('formal_arg')

 def p_sheet_definition(p):
     'sheet_definition: SHEET SHEET_IDENT [sheet_init}'
     print('sheet_definition')

 def p_sheet_init(p):
     '''sheet_init: EQ sheet_init_list
                    | EQ INT_LITERAL MULT INT_LITERAL'''
     print('sheet_init')

 def p_sheet_init_list(p):
     'sheet_init_list: LCURLY sheet_row {sheet_row} RCURLY'
     print('sheet_init_list')

def p_sheet_row(p):
    'sheet_row: simple_expr {COMMA simple_expr}'
    print('sheet_row')

def p_range_definition(p):
    'range_definition: RANGE RANGE_IDENT [EQ range_expr]'
    print('range_definition')

def p_scalar_definition(p):
    'scalar_definition: SCALAR IDENT [EQ scalar_expr]'
    print('scalar-definition')

def p_statement_list(p):
    'statement_list: statement {statement}'
    print('statement_list')

def p_statement(p):
    '''statement:   PRINT_SHEET [INFO_STRING] SHEET_IDENT
                    | PRINT_RANGE [INFO_STRING] range_expr
                    | PRINT_SCALAR [INFO_STRING] scalar_expr
                    | IF scalar_expr THEN statement_list [ELSE statament_list] ENDIF
                    | WHILE scalar_expr DO statement_list DONE
                    | FOR range_list DO statement_list DONE
                    | subroutine_call
                    | RETURN (scalar-expr | range_expr)
                    | assignment'''
    print('statement')

def p_range_list(p):

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
