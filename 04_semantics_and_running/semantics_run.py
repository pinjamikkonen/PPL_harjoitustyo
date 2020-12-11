# Pinja Mikkonen 99219
# Priciples of Programming Languages
# Project Work - Phase 4

import sys
import syntax
from semantics_common import SymbolData, SemData

def run_program(tree, semdata):
    semdata.stack = []
    eval_node(tree, semdata)

def eval_node(node, semdata):
    symtbl = semdata.symtbl
    nodetype = node.nodetype

    if nodetype == 'program':
        for i in node.children_funcs_vars:
            eval_node(i, semdata)
        for i in node.children_stmt_list:
            eval_node(i, semdata)

    if nodetype == 'print_scalar':
        print(eval_node(node.child_expr, semdata))

    if nodetype == 'scalar_ref':
        return symtbl[node.child_name.value].defnode.child_init.value

    if nodetype[0:4] == 'oper':
        if len(nodetype) == 6:
            left = eval_node(node.child_left, semdata)
            right = eval_node(node.child_right, semdata)

            if nodetype[5] == '+':
                return left + right
            elif nodetype[5] == '-':
                return left - right
            elif nodetype[5] == '*':
                return left * right
            elif nodetype[5] == '/':
                return left / right

    if nodetype == 'decimal_number':
        return float(node.value)

    return None