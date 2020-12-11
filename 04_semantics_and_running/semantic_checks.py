# Pinja Mikkonen 99219
# Priciples of Programming Languages
# Project Work - Phase 4

import sys
import syntax

parser = syntax.parser

from semantics_common import visit_tree, SymbolData, SemData

# HOZ @ SELF RIVILLÄ 237 YKSI RIVINUMEROKOMMENTTI
# TEE SILLE JOTAIN!!!!!

def add_vars(node, semdata):
    nodetype = node.nodetype

    if nodetype == 'scalar_definition':
        var_name = node.child_name.value

        if var_name in semdata.symtbl:
            return ("Error, variable name already in use! " + var_name + " on line nope")

        else:
            symdata = SymbolData('var', node)
            semdata.symtbl[var_name] = symdata
            node.symdata = symdata

    elif nodetype == 'scalar_assign':
        var_name = node.child_var.child_name.value
        if var_name not in semdata.symtbl:
            return ("Error, variable uninitialized! " + var_name)
        else:
            semdata.symtbl[var_name].defnode.child_init.value = node.child_expr.value

    elif nodetype == 'subroutine_def':
        var_name = node.child_name.value
        if var_name in semdata.symtbl:
            return ("Error, subroutine name already in use! " + var_name + " on line nope")
        else:
            symdata = SymbolData('subroutine', node)
            semdata.symtbl[var_name] = symdata
            node.symdata = symdata

    elif nodetype == 'subroutine_call':
        var_name = node.child_name.value
        if var_name not in semdata.symtbl:
            return ("Error, subroutine uninitialized! " + var_name)
        else:
            print("tyyppi " + semdata.symtbl[var_name].defnode.nodetype)
            if semdata.symtbl[var_name].defnode.nodetype is not 'subroutine_def':
                return ("Error, subroutine being called as a function!")


    elif nodetype == 'function_def':
        var_name = node.child_name.value
        if var_name in semdata.symtbl:
            return ("Error, function name already in use! " + var_name)
        else:
            symdata = SymbolData('func', node)
            semdata.symtbl[var_name] = symdata
            node.symdata = symdata

    elif nodetype == 'function_call':
        var_name = node.child_name.value
        if var_name not in semdata.symtbl:
            return ("Error, function name uninitialized " + var_name)
        else:
            if semdata.symtbl[var_name].defnode.nodetype is not 'function_def':
                return ("Error, function being called as a function!")


def print_symbol_table(semdata, title):
    print(title)
    for name, data in semdata.symtbl.items():
        print(name, ":")
        for attr, value in vars(data).items():
            printvalue = value
            if hasattr(value, "nodetype"):
                printvalue = value.nodetype
                if hasattr(value, "lineno"):
                    printvalue = printvalue + ", line " + str(value.lineno)
            print("  ", attr, "=", printvalue)


def semantic_checks(tree, semdata):
    semdata.plus_level = 0
    visit_tree(tree, add_vars, None, semdata)