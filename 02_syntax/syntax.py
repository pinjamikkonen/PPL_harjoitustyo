# Pinja Mikkonen 99219
# Priciples of Programming Languages
# Project Work - Phase 2

import sys
import ply.yacc as yacc
import lexer

tokens = lexer.tokens

def p_program(p):
    '''program :    statement_list
                    | function_or_variable_definitions statement_list'''
    print('program')

def p_function_or_variable_definitions(p):
    '''function_or_variable_definitions :   empty
                                            | function_or_variable_definition
                                            | function_or_variable_definitions function_or_variable_definition'''

def p_function_or_variable_definition(p):
    '''function_or_variable_definition : variable_definition
                                        | function_definition
                                        | subroutine_definition'''

def p_variable_definitions(p):
    '''variable_definitions :   empty
                                | variable_definition
                                | variable_definitions variable_definition'''

def p_variable_definition(p):
    '''variable_definition : scalar_definition
                            | range_definition
                            | sheet_definition'''
    print('variable_definition(', p[1], ')')

def p_function_definition(p):
    '''function_definition :    FUNCTION FUNC_IDENT LSQUARE RSQUARE RETURN SCALAR IS variable_definitions statement_list END
                                | FUNCTION FUNC_IDENT LSQUARE RSQUARE RETURN RANGE IS variable_definitions statement_list END
                                | FUNCTION FUNC_IDENT LSQUARE formals RSQUARE RETURN SCALAR IS variable_definitions statement_list END
                                | FUNCTION FUNC_IDENT LSQUARE formals RSQUARE RETURN RANGE IS variable_definitions statement_list END'''
    print('function_definition(', p[2], ')')

def p_subroutine_definition(p):
    '''subroutine_definition :  SUBROUTINE FUNC_IDENT LSQUARE RSQUARE IS variable_definitions statement_list END
                                | SUBROUTINE FUNC_IDENT LSQUARE formals RSQUARE IS variable_definitions statement_list END'''
    print('subroutine_definition(', p[2], ')')

def p_formals(p):
    '''formals : formal_arg
                | formal_arg COMMA formal_arg
                | formals COMMA formal_arg'''

def p_formal_arg(p):
     '''formal_arg : IDENT COLON SCALAR
                    | RANGE_IDENT COLON RANGE
                    | SHEET_IDENT COLON SHEET'''

def p_sheet_definition(p):
    'sheet_definition : SHEET SHEET_IDENT sheet_inits'
    print('sheet_definition')

def p_sheet_inits(p):
    '''sheet_inits : empty
                    | sheet_init
                    | sheet_inits sheet_init'''

def p_sheet_init(p):
    '''sheet_init :  EQ sheet_init_list
                    | EQ INT_LITERAL MULT INT_LITERAL'''

def p_sheet_init_list(p):
    'sheet_init_list : LCURLY sheet_row sheet_rows RCURLY'

def p_sheet_rows(p):
    '''sheet_rows : empty
                    | sheet_row
                    | sheet_rows sheet_row'''

def p_sheet_row(p):
    '''sheet_row :  simple_expr
                    | simple_expr COMMA simple_expr
                    | sheet_row COMMA simple_expr'''

def p_range_definition(p):
    '''range_definition :   RANGE RANGE_IDENT
                            | RANGE RANGE_IDENT EQ range_expr'''

def p_scalar_definition(p):
    '''scalar_definition :  SCALAR IDENT
                            | SCALAR IDENT EQ scalar_expr'''

def p_statement_list(p):
    '''statement_list : statement
                        | statement_list statement'''

def p_statement(p):
    '''statement :   PRINT_SHEET SHEET_IDENT
                    | PRINT_SHEET INFO_STRING SHEET_IDENT
                    | PRINT_RANGE range_expr
                    | PRINT_RANGE INFO_STRING range_expr
                    | PRINT_SCALAR scalar_expr
                    | PRINT_SCALAR INFO_STRING scalar_expr
                    | IF scalar_expr THEN statement_list ENDIF
                    | IF scalar_expr THEN statement_list ELSE statement_list ENDIF
                    | WHILE scalar_expr DO statement_list DONE
                    | FOR range_list DO statement_list DONE
                    | subroutine_call
                    | RETURN scalar_expr
                    | RETURN range_expr
                    | assignment'''
    print('statement (', ,')')

def p_range_list(p):
    '''range_list : range_expr
                    | range_list COMMA range_expr'''
    print('range_list')

def p_arguments(p):
    '''arguments :  arg_expr
                    | arguments COMMA arg_expr'''
    print('argument_expression')

def p_arg_expr(p):
    '''arg_expr :   scalar_expr
                    | range_expr
                    | SHEET_IDENT'''
    print('arg_expr')

def p_subroutine_call(p):
    '''subroutine_call : FUNC_IDENT LSQUARE RSQUARE
                         | FUNC_IDENT LSQUARE arguments RSQUARE'''
    print('subroutine_call(', p[1], ')')

def p_assignment(p):
    '''assignment :  IDENT ASSIGN scalar_expr
                    | cell_ref ASSIGN scalar_expr
                    | RANGE_IDENT ASSIGN range_expr
                    | SHEET_IDENT ASSIGN SHEET_IDENT'''
    print('assignment(', p[1], ')')

def p_range_expr(p):
    '''range_expr :  RANGE_IDENT
                    | RANGE cell_ref DOTDOT cell_ref
                    | LSQUARE function_call RSQUARE
                    | range_expr LSQUARE INT_LITERAL COMMA INT_LITERAL RSQUARE'''
    print('range_expr')

def p_cell_ref(p):
    '''cell_ref :    SHEET_IDENT SQUOTE COORDINATE_IDENT
                    | DOLLAR
                    | DOLLAR COLON RANGE_IDENT'''
    print('cell_ref')

def p_scalar_expr(p):
    '''scalar_expr :    simple_expr
                        | simple_expr EQ simple_expr
                        | simple_expr NOTEQ simple_expr
                        | simple_expr LT simple_expr
                        | simple_expr LTEQ simple_expr
                        | simple_expr GT simple_expr
                        | simple_expr GTEQ simple_expr'''
    print('scalar_expr')

def p_simple_expr(p):
    '''simple_expr :    term
                        | term PLUS term
                        | term MINUS term'''
    print('simple_expr')

def p_term(p):
    '''term :   factor
                | factor MULT factor
                | factor DIV factor'''
    print('term')

def p_factor(p):
    '''factor : atom
                | MINUS atom'''
    print('factor')

def p_atom(p):
    '''atom :    IDENT
                | DECIMAL_LITERAL
                | function_call
                | cell_ref
                | NUMBER_SIGN range_expr
                | LPAREN scalar_expr RPAREN'''
    print('atom(', p[1], ')')

def p_function_call(p):
    '''function_call :  FUNC_IDENT LSQUARE RSQUARE
                        | FUNC_IDENT LSQUARE arguments RSQUARE'''
    if len(p) == 4:
        print('function call()')
    else:
        print('function call(', p[3], ')')

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p != None:
        print("{%s}: Syntax Error(token: '%s')" % p.lineno, p.value)
        sys.exit()
    else:
        print('unexpected end on input')

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
        data = codecs.open(ns.file, encoding='utf-8').read()
        result = parser.parse(data, lexer=lexer.lexer, debug=False)
        if result is None:
            print('syntax OK')
