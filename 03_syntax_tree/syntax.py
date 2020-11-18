# Pinja Mikkonen 99219
# Priciples of Programming Languages
# Project Work - Phase 3

import sys
import ply.yacc as yacc
import lexer
import tree_print

tokens = lexer.tokens

class Node:
    def __init__(self, typestr):
        self.nodetype = typestr

# Definition of program
def p_program1(p):
    'program : statement_list'
    p[0] = Node('program')
    p[0].children_funcs_vars = []
    p[0].children_stmt_list = [p[1]]

def p_program2(p):
    'program : function_or_variable_definition program'
    p[0] = p[2]
    p[0].children_funcs_vars.insert(0, p[1])

# {} - None or multiple definitions
# hox ihan vaan p[0] = [p[1]]
#def p_function_or_variable_definitions(p):
##    '''function_or_variable_definitions :   function_or_variable_definition
 #                                           | function_or_variable_definitions function_or_variable_definition'''
#   if len(p) == 2:
#        p[0] = p[1]
#    else:
#        p[0] =

# Function or variable definition
def p_function_or_variable_definition(p):
    '''function_or_variable_definition : variable_definition
                                        | function_definition
                                        | subroutine_definition'''
    p[0] = p[1]

# {} - None or multiple definitions
def p_variable_definitions(p):
    '''variable_definitions :   empty
                                | variable_definition
                                | variable_definitions variable_definition'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 2:
        p[0] = Node('expr')
        p[0] = p[1]
        p[0].children_exprs = [p[2]]

# Variable definition
def p_variable_definition(p):
    '''variable_definition : scalar_definition
                            | range_definition
                            | sheet_definition'''
    p[0] = p[1]

# Function definition
def p_function_definition(p):
    '''function_definition :    FUNCTION FUNC_IDENT LSQUARE RSQUARE RETURN SCALAR IS variable_definitions statement_list END
                                | FUNCTION FUNC_IDENT LSQUARE RSQUARE RETURN RANGE IS variable_definitions statement_list END
                                | FUNCTION FUNC_IDENT LSQUARE formals RSQUARE RETURN SCALAR IS variable_definitions statement_list END
                                | FUNCTION FUNC_IDENT LSQUARE formals RSQUARE RETURN RANGE IS variable_definitions statement_list END'''
    #p[0] = Node('function')
    p[0].value = p[2]
    #p[0].children_ = [p[8], p[9]]

# Subroutine definition
def p_subroutine_definition1(p):
    'subroutine_definition :  SUBROUTINE FUNC_IDENT LSQUARE RSQUARE IS variable_definitions statement_list END'

    p[0] = Node('subroutine')
    p[0].value = p[2]
    p[0].children_vars = [p[7]]
    p[0].children_stmts = [p[8]]

def p_subroutine_definition2(p):
    'subroutine_definition : SUBROUTINE FUNC_IDENT LSQUARE formals RSQUARE IS variable_definitions statement_list END'
    p[0] = Node('subroutine')
    p[0].value = p[2]
    p[0].children_frmls = [p[4]]
    p[0].children_vars = [p[7]]
    p[0].children_stmts = [p[8]]

# Formals
def p_formals(p):
    '''formals : formal_arg
                | formal_arg COMMA formal_arg
                | formals COMMA formal_arg'''
    if len(p) == 2:
        p[0] = p[1]
    if len(p) > 2:
        p[0] = p[1]
        p[0].children_frmls.append(p[3])


# Formal arguments
def p_formal_arg(p):
     '''formal_arg : IDENT COLON SCALAR
                    | RANGE_IDENT COLON RANGE
                    | SHEET_IDENT COLON SHEET'''
     p[0] = Node('formal_arg')
     p[0].value = p[1]

# Sheet definition
def p_sheet_definition(p):
    '''sheet_definition : SHEET SHEET_IDENT
                          | SHEET SHEET_IDENT sheet_inits'''
    p[0] = Node('sheet_definition')
    p[0].child_name = Node('SHEET')
    p[0].child_name.value = p[2]
    if len(p) > 3:
        p[0].child_inits = p[3]

# {} - None or multiple sheet initializations
def p_sheet_inits(p):
    '''sheet_inits : sheet_init
                    | sheet_inits sheet_init'''
    if len(p) == 2:
        p[0] = Node('sheet_init')
        p[0].children_rows = []
    else:
        p[0] = p[1]
        p[0].children_rows.insert(0, p[2])

# Sheet initialization
def p_sheet_init(p):
    '''sheet_init :  EQ sheet_init_list
                    | EQ INT_LITERAL MULT INT_LITERAL'''
    p[0] = Node('sheet_init')

# Sheet initialization list
def p_sheet_init_list(p):
    'sheet_init_list : LCURLY sheet_rows RCURLY'
    p[0] = Node('sheet_init_list')

# {} - None or multiple sheet rows
def p_sheet_rows(p):
    '''sheet_rows : sheet_row
                    | sheet_rows sheet_row'''
    p[0] = Node('sheet_row')

# Sheet rows
def p_sheet_row(p):
    '''sheet_row :  simple_expr
                    | sheet_row COMMA simple_expr'''
    if len(p) == 2:
        p[0] = Node('col_init_list')
        p[0].children_cols = []
    else:
        p[0] = p[1]
        p[0].children_cols.insert(0, p[3])


# Range definition
def p_range_definition(p):
    '''range_definition :   RANGE RANGE_IDENT
                            | RANGE RANGE_IDENT EQ range_expr'''

# Scalar definition
def p_scalar_definition(p):
    '''scalar_definition :  SCALAR IDENT
                            | SCALAR IDENT EQ scalar_expr'''
    p[0] = Node('scalar_definition')
    p[0].child_name = Node('IDENT')
    p[0].child_name.value = p[2]

    if len(p) > 4:
        p[0].child_init = p[4]

# Statement list
def p_statement_list(p):
    '''statement_list : statement
                        | statement statement_list'''
    if len(p) == 2:
        p[0] = p[1]
        p[0].children_stmt_list = []
    else:
        p[0] = p[2]
        p[0].children_stmt_list.insert(0, p[1])

# Statements
def p_statement(p):
    '''statement :   PRINT_SHEET SHEET_IDENT
                    | PRINT_SHEET INFO_STRING SHEET_IDENT
                    | PRINT_RANGE range_expr
                    | PRINT_RANGE INFO_STRING range_expr
                    | PRINT_SCALAR scalar_expr
                    | IF scalar_expr THEN statement_list ENDIF
                    | IF scalar_expr THEN statement_list ELSE statement_list ENDIF
                    | WHILE scalar_expr DO statement_list DONE
                    | FOR range_list DO statement_list DONE
                    | subroutine_call
                    | RETURN scalar_expr
                    | RETURN range_expr
                    | assignment'''
    # Assignments aren't printed
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('statement ')
        p[0].value = p[1]

def p_statement2(p):
    'statement : PRINT_SCALAR INFO_STRING scalar_expr'
    p[0] = Node('statement')
    p[0].child_infostr = Node('infostring')
    p[0].child_infostr.value = p[2]
    p[0].child_expr = p[3]

# Range list
def p_range_list(p):
    '''range_list : range_expr
                    | range_list COMMA range_expr'''

# Argument list
def p_arguments(p):
    '''arguments :  arg_expr
                    | arguments COMMA arg_expr'''

# Argument expression
def p_arg_expr(p):
    '''arg_expr :   scalar_expr
                    | range_expr
                    | SHEET_IDENT'''

# Subroutine call
def p_subroutine_call(p):
    '''subroutine_call : FUNC_IDENT LSQUARE RSQUARE
                         | FUNC_IDENT LSQUARE arguments RSQUARE'''

# Printable assignments
def p_assignment1(p):
    '''assignment :     IDENT ASSIGN scalar_expr
                        | RANGE_IDENT ASSIGN range_expr
                        | SHEET_IDENT ASSIGN SHEET_IDENT
                        | cell_ref ASSIGN scalar_expr'''
    p[0] = Node('scalar_assign')
    p[0].child_left = p[1]
    p[0].child_right = p[3]

# Nonprintable assignments
#def p_assignment2(p):
#    'assignment : cell_ref ASSIGN scalar_expr'

# Range expression
def p_range_expr(p):
    '''range_expr :  RANGE_IDENT
                    | RANGE cell_ref DOTDOT cell_ref
                    | LSQUARE function_call RSQUARE
                    | range_expr LSQUARE INT_LITERAL COMMA INT_LITERAL RSQUARE'''

# Cell reference
def p_cell_ref(p):
    '''cell_ref :    SHEET_IDENT SQUOTE COORDINATE_IDENT
                    | DOLLAR
                    | DOLLAR COLON RANGE_IDENT'''

# Scalar expression
def p_scalar_expr(p):
    '''scalar_expr :    simple_expr
                        | simple_expr EQ simple_expr
                        | simple_expr NOTEQ simple_expr
                        | simple_expr LT simple_expr
                        | simple_expr LTEQ simple_expr
                        | simple_expr GT simple_expr
                        | simple_expr GTEQ simple_expr'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('oper ' + p[2])
        p[0].child_left = p[1]
        p[0].child_right = p[3]

# Simple expression
def p_simple_expr(p):
    '''simple_expr :    term
                        | simple_expr PLUS term
                        | simple_expr MINUS term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('oper ' + p[2])
        p[0].child_left = p[1]
        p[0].child_right = p[3]

# Term definition
def p_term(p):
    '''term :   factor
                | term MULT factor
                | term DIV factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('oper ' + p[2])
        p[0].child_left = p[1]
        p[0].child_right = p[3]

# Factor definition
def p_factor(p):
    '''factor : atom
                | MINUS atom'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('oper ' + p[1])
        p[0].child_ = p[2]

# Nonprintable atoms
def p_atom1(p):
    '''atom :   function_call
                | cell_ref'''
    p[0] = p[1]

def p_atom2(p):
    '''atom :   NUMBER_SIGN range_expr
                | LPAREN scalar_expr RPAREN'''
    p[0] = p[2]

# Printable atoms
def p_atom3(p):
    'atom : IDENT'
    p[0] = Node('identifier')
    p[0].value = p[1]
    p[0].lineno = p.lineno(1)

def p_atom4(p):
    'atom : DECIMAL_LITERAL'
    p[0] = Node('decimal_number')
    p[0].value = p[1]
    p[0].lineno = p.lineno(1)

# Function calls
def p_function_call(p):
    '''function_call :  FUNC_IDENT LSQUARE RSQUARE
                        | FUNC_IDENT LSQUARE arguments RSQUARE'''
    p[0] = Node('function_call')
    p[0].child_name = p[1]
    if len(p) > 4:
        p[0].children_args = p[3]

# Empty definition used in {} -statements
def p_empty(p):
    'empty :'
    pass

# Error handling
def p_error(p):
    if p != None:
        print('{', p.lineno, '}: Syntax Error(token: \'', p.value, '\')')
        sys.exit()
    else:
        print('Unexpected end on input')
        sys.exit()

parser = yacc.yacc()

if __name__ == '__main__':
    import argparse, codecs

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-t', '--treetype', help='type of output tree (unicode/ascii/dot)')
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this' )
    group.add_argument('-f', '--file', help='filename to process')
    group.add_argument('--prayer', help='rukous Ahto Simakuutiolle')
    ns = arg_parser.parse_args()

    outformat = "unicode"

    if ns.treetype:
      outformat = ns.treetype

    if ns.who == True:
        print('99219 Pinja Mikkonen :)')
    elif ns.file is None:
        arg_parser.print_help()
    elif ns.prayer == True:
        print('Varjelkoon Ahto Simakuutio meitä')
    else:
        data = codecs.open(ns.file, encoding='utf-8').read()
        result = parser.parse(data, lexer=lexer.lexer, debug=False)

        tree_print.treeprint(result, outformat)