# Pinja Mikkonen 99219
# Priciples of Programming Languages
# Project Work - Phase 1

import sys
import ply.lex as lex

#Reserved words
reserved = {
    'sheet': 'SHEET',
    'scalar': 'SCALAR',
    'range': 'RANGE',
    'do': 'DO',
    'done': 'DONE',
    'is': 'IS',
    'while': 'WHILE',
    'for': 'FOR',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'endif': 'ENDIF',
    'function': 'FUNCTION',
    'subroutine': 'SUBROUTINE',
    'return': 'RETURN',
    'end': 'END',
    'print_sheet': 'PRINT_SHEET',
    'print_scalar': 'PRINT_SCALAR',
    'print_range': 'PRINT_RANGE'
}

#Token list
tokens = [
    'ASSIGN',
    'LPAREN',
    'RPAREN',
    'LSQUARE',
    'RSQUARE',
    'LCURLY',
    'RCURLY',
    'COMMA',
    'DOTDOT',
    'SQUOTE',
    'COLON',
    'DOLLAR',
    'NUMBER_SIGN',
    'EQ',
    'NOTEQ',
    'LT',
    'LTEQ',
    'GT',
    'GTEQ',
    'PLUS',
    'MINUS',
    'MULT',
    'DIV',
    'INFO_STRING',
    'COORDINATE_IDENT',
    'DECIMAL_LITERAL',
    'INT_LITERAL',
    'RANGE_IDENT',
    'SHEET_IDENT',
    'FUNC_IDENT',
    'IDENT',
] + list(reserved.values())

# One or two letter tokens
t_ASSIGN = r'\:='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_LCURLY = r'\{'
t_RCURLY = r'\}'

t_COMMA = r'\,'
t_DOTDOT = r'\..'
t_SQUOTE = r'\''
t_COLON = r'\:'
t_DOLLAR = r'\$'
t_NUMBER_SIGN = r'\#'

t_EQ = r'\='
t_NOTEQ = r'\!='
t_LT = r'\<'
t_LTEQ = r'\<='
t_GT = r'\>'
t_GTEQ = r'\>='
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULT = r'\*'
t_DIV = r'\/'

t_DECIMAL_LITERAL = r'-?[0-9]+\.[0-9]'
t_INT_LITERAL = r'-?[0-9]+'

# Comments get ignored
def t_COMMENT(t):
    r'\.\.\.(.|\n)*?\.\.\.'
    pass

# Info string
def t_INFO_STRING(t):
    r'!.*!'
    t.type = reserved.get(t.value, 'INFO_STRING')
    return t

# New line
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

#Ignored characters
t_ignore = ' \t\r'

# Longer tokens
def t_COORDINATE_IDENT(t):
    r'([A-Z]{1,2}[0-9]{1,3})'
    t.type = reserved.get(t.value, 'COORDINATE_IDENT')
    return t

def t_RANGE_ID(t):
    r'(\_[a-zA-Z0-9]+)'
    t.type = reserved.get(t.value, 'RANGE_IDENT')
    return t

def t_FUNC_ID(t):
    r'([A-Z][a-z0-9_]+)'
    t.type = reserved.get(t.value, 'FUNC_IDENT')
    return t

def t_SHEET_ID(t):
    r'([A-Z]+)'
    t.type = reserved.get(t.value, 'SHEET_IDENT')
    return t

def t_IDENT(t):
    r'[a-z][a-zA-Z0-9_]+'
    t.type = reserved.get(t.value, 'IDENT')
    return t

# Error handling
def t_error(t):
    print('Illegal character \'%s\' at line ' % t.value[0], t.lexer.lineno)
    sys.exit()

# Build lexer
lexer = lex.lex()

# Main
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='Name of author')
    group.add_argument('-f', '--file', help='Filename to process')

    ns = parser.parse_args()
    if ns.who == True:
        print('99219 Pinja Mikkonen :)')
    elif ns.file is None:
        parser.print_help()
    else:
        with open(ns.file, 'r', encoding='utf-8') as INFILE:
            data = INFILE.read()

        lexer.input(data)

        while True:
            token = lexer.token()
            if token is None:
                break
            print(token)