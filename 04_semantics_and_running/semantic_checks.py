# Pinja Mikkonen 99219
# Priciples of Programming Languages
# Project Work - Phase 4

import syntax
import re

parser = syntax.parser
from semantics_common import visit_tree, SymbolData, SemData

def add_vars(node, semdata):
    nodetype = node.nodetype

    # Scalar checks
    if nodetype == 'scalar_definition':
        var_name = node.child_name.value

        # Check if name is already in use
        if var_name in semdata.symtbl:
            return "Error, variable name already in use: " + var_name

        # Initialize the value
        else:
            symdata = SymbolData('var', node)
            semdata.symtbl[var_name] = symdata
            node.symdata = symdata

    # Assign scalar values
    elif nodetype == 'scalar_assign':
        var_name = node.child_var.child_name.value

        # Check if variable has not been initialized
        if var_name not in semdata.symtbl:
            return "Error, variable uninitialized: " + var_name

    # Sheet definition
    elif nodetype == 'sheet_definition':
        var_name = node.child_name.value

        # Check if variable name is already in use
        if var_name in semdata.symtbl:
            return "Error, sheet name already in use: " + var_name

        # Check that all rows are the same length
        else:
            rowlen = len(node.children_init[0].children_rows[0].children_cols)
            for i in range(0, len(node.children_init)):
                for j in range(0, len(node.children_init[i].children_rows)):
                    if rowlen is not len(node.children_init[i].children_rows[j].children_cols):
                        return "Error, all sheet rows not the same length"

            # If test passes initialize the sheet
            symdata = SymbolData('sheet', node)
            semdata.symtbl[var_name] = symdata
            node.symdata = symdata

    # Range definition
    elif nodetype == 'range_definition':
        var_name = node.child_name.value

        # Check if variable has not been initialized
        if var_name in semdata.symtbl:
            return "Error, range name already in use: " + var_name

        # Initialize the subroutine
        else:
            symdata = SymbolData('range', node)
            semdata.symtbl[var_name] = symdata
            node.symdata = symdata

    elif nodetype == 'range':
        cell1 = node.child_coord1
        cell2 = node.child_coord2

        # Check if cells refer to the same sheet
        if hasattr(cell1, 'child_name') and hasattr(cell2, 'child_name'):
            if cell1.child_name.value != cell2.child_name.value:
                return "Error, range cells must refer to the same sheet"

            # Check that range refers to either a horizontal or vertical range
            # ie., either the row or column indicator matches
            else:
                coord1 = cell1.child_coord.value
                coord2 = cell2.child_coord.value

                # Lambda that searches strings x and y for regexp r and checks if returned matches are the same
                checkrange = lambda x, y, r: re.search(r, x).group() is re.search(r, y).group()

                if not (checkrange(coord1, coord2, r'[A-Z]{1,2}') or checkrange(coord1, coord2, r'[0-9]{1,3}')):
                    return "Error, illegal range"
                else:
                    return None
        else:
            return None

    # Subroutine definition
    elif nodetype == 'subroutine_def':
        var_name = node.child_name.value

        # Check if function name is already in use
        if var_name in semdata.symtbl:
            return "Error, subroutine name already in use: " + var_name

        # Initialize the subroutine
        else:
            symdata = SymbolData('subroutine', node)
            semdata.symtbl[var_name] = symdata
            node.symdata = symdata

    # Subroutine call
    elif nodetype == 'subroutine_call':
        var_name = node.child_name.value

        # Check if subroutine has been initialized
        if var_name not in semdata.symtbl:
            return "Error, subroutine uninitialized " + var_name
        else:

            # Check if subroutine is being called as a function
            if semdata.symtbl[var_name].defnode.nodetype is not 'subroutine_def':
                return "Error, subroutine being called as a function"

            # Check if the number of parameters and arguments is the same
            else:
                if hasattr(node, "children_args") and hasattr(semdata.symtbl[var_name].defnode, "children_formals"):
                    formals = len(semdata.symtbl[var_name].defnode.children_formals)
                    args = len(node.children_args)

                    if formals != args:
                        return "Error, subroutine has wrong number of arguments!"

                # If only arguments or formal arguments exist raise error
                elif hasattr(node, "children_args") or hasattr(semdata.symtbl[var_name].defnode, "children_formals"):
                    return "Error, subroutine call has wrong number of arguments"

    # Function definition
    elif nodetype == 'function_def':
        var_name = node.child_name.value

        # Check if function name is already in use
        if var_name in semdata.symtbl:
            return "Error, function name already in use " + var_name

        # Initialize the function
        else:
            symdata = SymbolData('func', node)
            semdata.symtbl[var_name] = symdata
            node.symdata = symdata

    # Function call
    elif nodetype == 'function_call':
        var_name = node.child_name.value

        # Check if function name is already in use
        if var_name not in semdata.symtbl:
            return "Error, function name uninitialized " + var_name

        # Check if function is being called as a subroutine
        else:
            if semdata.symtbl[var_name].defnode.nodetype is not 'function_def':
                return "Error, function being called as a subroutine"

            # Check if the number of arguments is the same as parameters
            if hasattr(node, "children_args") and hasattr(semdata.symtbl[var_name].defnode, "children_formals"):
                formals = len(semdata.symtbl[var_name].defnode.children_formals)
                args = len(node.children_args)

                if formals != args:
                    return "Error, function has wrong number of arguments!"

            # If only arguments or formal arguments exist raise error
            elif hasattr(node, "children_args") or hasattr(semdata.symtbl[var_name].defnode, "children_formals"):
                return "Error, function call has wrong number of arguments"


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