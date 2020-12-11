# Pinja Mikkonen 99219
# Priciples of Programming Languages
# Project Work - Phase 4

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
    p[0].children_stmt_list = p[1]

def p_program2(p):
    'program : function_or_variable_definition program'
    p[0] = p[2]
    p[0].children_funcs_vars.insert(0, p[1])

# Function or variable definition
def p_function_or_variable_definition(p):
    '''function_or_variable_definition : variable_definition
                                        | function_definition
                                        | subroutine_definition'''
    p[0] = p[1]

# One or multiple variable definitions
def p_variable_definitions(p):
    '''variable_definitions :   variable_definition
                                | variable_definitions variable_definition'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 2:
        p[0] = p[1]
        p[0].children_vars.append(p[2])

# Variable definition
def p_variable_definition(p):
    '''variable_definition : scalar_definition
                            | range_definition
                            | sheet_definition'''
    p[0] = p[1]

# Function definition - no formals
def p_function_definition1(p):
    '''function_definition :    FUNCTION FUNC_IDENT LSQUARE RSQUARE RETURN SCALAR IS statement_list END
                                | FUNCTION FUNC_IDENT LSQUARE RSQUARE RETURN RANGE IS statement_list END
                                | FUNCTION FUNC_IDENT LSQUARE RSQUARE RETURN SCALAR IS variable_definitions statement_list END
                                | FUNCTION FUNC_IDENT LSQUARE RSQUARE RETURN RANGE IS variable_definitions statement_list END'''
    p[0] = Node('function_def')
    p[0].child_name = Node('FUNC_IDENT')
    p[0].child_name.value = p[2]
    p[0].child_rettype = Node('rettype')
    p[0].child_rettype.value = p[6]

    # No variables
    if len(p) == 10:
        p[0].children_stmt_list = p[8]

    # Variables and statement list
    else:
        p[0].children_vars = p[8]
        p[0].children_stmt_list = p[9]

# Function definition - with formals
def p_function_definition2(p):
    '''function_definition :    FUNCTION FUNC_IDENT LSQUARE formals RSQUARE RETURN SCALAR IS statement_list END
                                | FUNCTION FUNC_IDENT LSQUARE formals RSQUARE RETURN RANGE IS statement_list END
                                | FUNCTION FUNC_IDENT LSQUARE formals RSQUARE RETURN SCALAR IS variable_definitions statement_list END
                                | FUNCTION FUNC_IDENT LSQUARE formals RSQUARE RETURN RANGE IS variable_definitions statement_list END'''
    p[0] = Node('function_def')
    p[0].child_name = Node('FUNC_IDENT')
    p[0].child_name.value = p[2]
    p[0].children_formals = p[4]
    p[0].child_rettype = Node('rettype')
    p[0].child_rettype.value = p[7]

    # No variables
    if len(p) == 11:
        p[0].children_stmt_list = p[9]

    # Variables and statement list
    else:
        p[0].children_vars = p[9]
        p[0].children_stmt_list = p[10]

# Subroutine definition - no formals
def p_subroutine_definition1(p):
    '''subroutine_definition :  SUBROUTINE FUNC_IDENT LSQUARE RSQUARE IS statement_list END
                                | SUBROUTINE FUNC_IDENT LSQUARE RSQUARE IS variable_definitions statement_list END'''
    p[0] = Node('subroutine_def')
    p[0].child_name = Node('FUNC_IDENT')
    p[0].child_name.value = p[2]

    # No variables
    if len(p) == 8:
        p[0].children_stmts = p[6]

    # Variables and statement list
    else:
        p[0].children_vars = p[6]
        p[0].children_stmts = p[7]

# Subroutine definition - with formals
def p_subroutine_definition2(p):
    '''subroutine_definition :  SUBROUTINE FUNC_IDENT LSQUARE formals RSQUARE IS statement_list END
                                | SUBROUTINE FUNC_IDENT LSQUARE formals RSQUARE IS variable_definitions statement_list END'''
    p[0] = Node('subroutine_def')
    p[0].child_name = Node('FUNC_IDENT')
    p[0].child_name.value = p[2]
    p[0].children_frmls = p[4]

    # No variables
    if len(p) == 9:
        p[0].children_stmts = p[7]

    # Variables and statement list
    else:
        p[0].children_vars = p[7]
        p[0].children_stmts = p[8]

# Formals
def p_formals(p):
    '''formals : formal_arg
                | formals COMMA formal_arg'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[3])

# Formal arguments
def p_formal_arg1(p):
     'formal_arg : IDENT COLON SCALAR'
     p[0] = Node('formal_arg')
     p[0].child_name = Node('IDENT')
     p[0].child_name.value = p[1]

def p_formal_arg2(p):
    'formal_arg : RANGE_IDENT COLON RANGE'
    p[0] = Node('formal_arg')
    p[0].child_name = Node('RANGE_IDENT')
    p[0].child_name.value = p[1]

def p_formal_arg(p):
     'formal_arg : SHEET_IDENT COLON SHEET'
     p[0] = Node('formal_arg')
     p[0].child_name = Node('SHEET_IDENT')
     p[0].child_name.value = p[1]

# Sheet definition
def p_sheet_definition(p):
    '''sheet_definition : SHEET SHEET_IDENT
                          | SHEET SHEET_IDENT sheet_inits'''
    p[0] = Node('sheet_definition')
    p[0].child_name = Node('SHEET_IDENT')
    p[0].child_name.value = p[2]
    if len(p) == 4:
        p[0].children_init = p[3]

# One or multiple sheet initializations
def p_sheet_inits(p):
    '''sheet_inits : sheet_init
                    | sheet_inits sheet_init'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[2])

# Sheet initialization
def p_sheet_init(p):
    '''sheet_init :  EQ sheet_init_list
                    | EQ INT_LITERAL MULT INT_LITERAL'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = Node('sheet_init_size')
        p[0].value = (p[2], p[4])

# Sheet initialization list
def p_sheet_init_list(p):
    'sheet_init_list : LCURLY sheet_rows RCURLY'
    p[0] = Node('sheet_init_list')
    p[0].children_rows = p[2]

# One or multiple sheet rows
def p_sheet_rows(p):
    '''sheet_rows : sheet_row
                    | sheet_rows sheet_row'''
    if len(p) == 2:
        p[0] = [p[1]]

    else:
        p[0] = p[1]
        p[0].append(p[2])

# Sheet rows
def p_sheet_row(p):
    '''sheet_row :  simple_expr
                    | sheet_row COMMA simple_expr'''
    if len(p) == 2:
        p[0] = Node('col_init_list')
        p[0].children_cols = [p[1]]

    else:
        p[0] = p[1]
        p[0].children_cols.append(p[3])


# Range definition
def p_range_definition(p):
    '''range_definition :   RANGE RANGE_IDENT
                            | RANGE RANGE_IDENT EQ range_expr'''
    p[0] = Node('range_definition')
    p[0].child_name = Node('RANGE_IDENT')
    p[0].child_name.value = p[2]

    if len(p) == 5:
        p[0].child_init = p[4]

# Scalar definition
def p_scalar_definition(p):
    '''scalar_definition :  SCALAR IDENT
                            | SCALAR IDENT EQ scalar_expr'''
    p[0] = Node('scalar_definition')
    p[0].child_name = Node('IDENT')
    p[0].child_name.value = p[2]
    # p[0].lineno = p.lineno(1)

    if len(p) == 5:
        p[0].child_init = p[4]

# Statement list
def p_statement_list(p):
    '''statement_list : statement
                        | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]

    else:
        p[0] = p[1]
        p[0].append(p[2])

# Print statements without infostring
def p_statement1(p):
    '''statement :   PRINT_SHEET SHEET_IDENT
                    | PRINT_RANGE range_expr
                    | PRINT_SCALAR scalar_expr'''
    if p[1] == 'print_sheet':
        p[0] = Node('print_sheet')
        p[0].child_expr = Node('sheet_ref')
        p[0].child_expr.child_name = Node('SHEET_IDENT')
        p[0].child_expr.child_name.value = p[2]

    elif p[1] == 'print_range':
        p[0] = Node('print_range')
        p[0].child_expr = p[2]

    elif p[1] == 'print_scalar':
        p[0] = Node('print_scalar')
        p[0].child_expr = p[2]

# Print statements with infostring
def p_statement2(p):
    '''statement :   PRINT_SHEET INFO_STRING SHEET_IDENT
                    | PRINT_RANGE INFO_STRING range_expr
                    | PRINT_SCALAR INFO_STRING scalar_expr'''

    if p[1] == 'print_sheet':
        p[0] = Node('print_sheet')
        p[0].child_infostr = Node('infostring')
        p[0].child_infostr.value = p[2]
        p[0].child_expr = Node('sheet_ref')
        p[0].child_expr.child_name = Node('SHEET_IDENT')
        p[0].child_expr.child_name.value = p[3]

    elif p[1] == 'print_range':
        p[0] = Node('print_range')
        p[0].child_infostr = Node('infostring')
        p[0].child_infostr.value = p[2]
        p[0].child_expr = p[3]

    elif p[1] == 'print_scalar':
        p[0] = Node('print_scalar')
        p[0].child_infostr = Node('infostring')
        p[0].child_infostr.value = p[2]
        p[0].child_expr = p[3]

# Assorted statements
def p_statement3(p):
    '''statement :  IF scalar_expr THEN statement_list ENDIF
                    | IF scalar_expr THEN statement_list ELSE statement_list ENDIF
                    | WHILE scalar_expr DO statement_list DONE
                    | FOR range_list DO statement_list DONE
                    | subroutine_call
                    | RETURN scalar_expr
                    | RETURN range_expr
                    | assignment'''

    # Pass assignment and subroutine on
    if len(p) == 2:
        p[0] = p[1]

    # if-statements
    elif p[1] == 'if':
        p[0] = Node('if_stmt')
        p[0].child_cond = p[2]
        p[0].children_then_list = p[4]
        if len(p) == 8:
            p[0].children_else_list = p[6]

    # while-statements
    elif p[1] == 'while':
        p[0] = Node('while_stmt')
        p[0].child_cond = p[2]
        p[0].children_do = p[4]

    # for-loops
    elif p[1] == 'for':
        p[0] = Node('for_stmt')
        p[0].children_ranges = p[2]
        p[0].children_stmt_list = p[4]

    # return statements
    elif p[1] == 'return':
        p[0] = Node('return')
        p[0].child_expr = p[2]

# Range list
def p_range_list(p):
    '''range_list : range_expr
                    | range_list COMMA range_expr'''
    if len(p) == 2:
        p[0] = [p[1]]

    else:
        p[0] = p[1]
        p[0].append(p[3])

# Argument list
def p_arguments(p):
    '''arguments :  arg_expr
                    | arguments COMMA arg_expr'''
    if len(p) == 2:
        p[0] = [p[1]]

    else:
        p[0] = p[1]
        p[0].append(p[3])

# Argument expression
def p_arg_expr1(p):
    '''arg_expr :   scalar_expr
                    | range_expr'''
    p[0] = p[1]

def p_arg_expr2(p):
    'arg_expr : SHEET_IDENT'
    p[0] = Node('sheet_ref')
    p[0].child_name = Node('SHEET_IDENT')
    p[0].child_name.value = p[1]

# Subroutine call
def p_subroutine_call(p):
    '''subroutine_call : FUNC_IDENT LSQUARE RSQUARE
                         | FUNC_IDENT LSQUARE arguments RSQUARE'''
    p[0] = Node('subroutine_call')
    p[0].child_name = Node('FUNC_IDENT')
    p[0].child_name.value = p[1]

    if len(p) == 5:
        p[0].children_args = p[3]

# Range assignments
def p_assignment1(p):
    'assignment : RANGE_IDENT ASSIGN range_expr'
    p[0] = Node('range_assign')
    p[0].child_var = Node('range_ref')
    p[0].child_var.child_name = Node('RANGE_IDENT')
    p[0].child_var.child_name.value = p[1]
    p[0].child_expr = p[3]

# Scalar assignments
def p_assignment2(p):
    'assignment : IDENT ASSIGN scalar_expr'
    p[0] = Node('scalar_assign')
    p[0].child_var = Node('scalar_ref')
    p[0].child_var.child_name = Node('IDENT')
    p[0].child_var.child_name.value = p[1]
    p[0].child_expr = p[3]

# Sheet assignments
def p_assignment3(p):
    'assignment : SHEET_IDENT ASSIGN SHEET_IDENT'
    p[0] = Node('sheet_assign')
    p[0].child_var = Node('sheet_ref')
    p[0].child_var.child_name = Node('SHEET_IDENT')
    p[0].child_var.child_name.value = p[1]

    p[0].child_expr = Node('sheet_ref')
    p[0].child_expr.child_name = Node('SHEET_IDENT')
    p[0].child_expr.child_name.value = p[3]

# Cell assignments
def p_assignment4(p):
    'assignment : cell_ref ASSIGN scalar_expr'
    p[0] = Node('cell_assign')
    p[0].child_cell = p[1]
    p[0].child_expr = p[3]

# Range expressions
def p_range_expr(p):
    '''range_expr :  RANGE_IDENT
                    | RANGE cell_ref DOTDOT cell_ref
                    | LSQUARE function_call RSQUARE
                    | range_expr LSQUARE INT_LITERAL COMMA INT_LITERAL RSQUARE'''
    if len(p) == 2:
        p[0] = Node('range_ref')
        p[0].child_name = Node('RANGE_IDENT')
        p[0].child_name.value = p[1]

    elif p[1] == 'range':
        p[0] = Node('range')
        p[0].child_coord1 = p[2]
        p[0].child_coord2 = p[4]

    elif p[1] == '[':
        p[0] = p[2]

    else:
        p[0] = Node('range_shift')
        p[0].value = (p[3], p[5])
        p[0].child_expr = p[1]

# Cell reference
def p_cell_ref(p):
    '''cell_ref :    SHEET_IDENT SQUOTE COORDINATE_IDENT
                    | DOLLAR
                    | DOLLAR COLON RANGE_IDENT'''
    if len(p) == 2:
        p[0] = Node('cell_ref')

    elif p[2] == '\'':
        p[0] = Node('cell_ref')
        p[0].child_name = Node('SHEET_IDENT')
        p[0].child_name.value = p[1]
        p[0].child_coord = Node('coord')
        p[0].child_coord.value = p[3]

    elif p[2] == ':':
        p[0] = Node('cell_ref')
        p[0].child_range_selector = Node('range_ref')
        p[0].child_range_selector.child_name = Node('RANGE_IDENT')
        p[0].child_range_selector.child_name.value = p[3]

# Scalar expression
def p_scalar_expr(p):
    '''scalar_expr :    simple_expr
                        | scalar_expr EQ simple_expr
                        | scalar_expr NOTEQ simple_expr
                        | scalar_expr LT simple_expr
                        | scalar_expr LTEQ simple_expr
                        | scalar_expr GT simple_expr
                        | scalar_expr GTEQ simple_expr'''
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
        p[0].child_value = p[2]

# Function calls and cell references get passed on
def p_atom1(p):
    '''atom :   function_call
                | cell_ref'''
    p[0] = p[1]

# Range and scalar expressions get passed on
def p_atom2(p):
    '''atom :   NUMBER_SIGN range_expr
                | LPAREN scalar_expr RPAREN'''
    p[0] = p[2]

# Identifiers
def p_atom3(p):
    'atom : IDENT'
    p[0] = Node('scalar_ref')
    p[0].child_name = Node('IDENT')
    p[0].child_name.value = p[1]

# Decimal numbers
def p_atom4(p):
    'atom : DECIMAL_LITERAL'
    p[0] = Node('decimal_number')
    p[0].value = p[1]

# Function calls
def p_function_call(p):
    '''function_call :  FUNC_IDENT LSQUARE RSQUARE
                        | FUNC_IDENT LSQUARE arguments RSQUARE'''
    p[0] = Node('function_call')
    p[0].child_name = Node('FUNC_IDENT')
    p[0].child_name.value = p[1]

    if len(p) == 5:
        p[0].children_args = p[3]

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
    group.add_argument('--prayer', action='store_true', help='Rukous Ahto Simakuutiolle')
    ns = arg_parser.parse_args()

    outformat = "unicode"

    if ns.treetype:
      outformat = ns.treetype

    if ns.who == True:
        print('99219 Pinja Mikkonen :)')
    elif ns.prayer == True:
        print('Ahto Simakuutio, joka olet koodissani\nPyhitetty olkoon sinun spagettisi\nTulkoon sinun errorisi\nTapahtukoon sinun kaatumisesi\nmyös loppupalautuksessa, niin kuin testauksessa')
    elif ns.file is None:
        arg_parser.print_help()
    else:
        data = codecs.open(ns.file, encoding='utf-8').read()
        result = parser.parse(data, lexer=lexer.lexer, debug=False)

        tree_print.treeprint(result, outformat)