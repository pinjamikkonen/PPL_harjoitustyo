# Pinja Mikkonen 99219
# Priciples of Programming Languages
# Project Work - Phase 4

from semantics_common import visit_tree, SymbolData, SemData

def run_program(tree, semdata):
    semdata.stack = []
    eval_node(tree, semdata)

def eval_node(node, semdata):
    symtbl = semdata.symtbl
    nodetype = node.nodetype

    # Execute program by iterating over the statements in the program
    if nodetype == 'program':
        for i in node.children_stmt_list:
            eval_node(i, semdata)
        return None

    # Execute function by iterating over the statements in the function
    elif nodetype == 'function_def':
        for i in node.children_stmt_list:
            eval_node(i, semdata)

    # Execute the function call by evaluating the function_def-node
    elif nodetype == 'function_call':
        return eval_node(symtbl[node.child_name.value].defnode, semdata)

    # Execute function by iterating over the statements in the subroutine
    elif nodetype == 'subroutine_def':
        for i in node.children_stmts:
            eval_node(i, semdata)

    # Execute the subroutine call by evaluating the subroutine_def-node
    elif nodetype == 'subroutine_call':
        return eval_node(symtbl[node.child_name.value].defnode, semdata)

    # Execute the if-statement
    elif nodetype == 'if_stmt':
        # Evaluate if the condition of the statement is true and execute the block if it is
        if eval_node(node.child_cond, semdata):
            for i in node.children_then_list:
                eval_node(i, semdata)

        #If if-else structure exists, then execute the else-block
        elif hasattr(node, "children_else_list"):
            for i in node.children_else_list:
                eval_node(i, semdata)

    #Execute while-statement
    elif nodetype == 'while_stmt':
        # Evaluate if the condition of the block is true and execute the statements if it is
        while eval_node(node.child_cond, semdata):
            for i in node.children_do:
                eval_node(i, semdata)

    # Print scalar expression
    elif nodetype == 'print_scalar':
        print(eval_node(node.child_expr, semdata))

    # Assign a new value to a scalar expression
    elif nodetype == 'scalar_assign':
        var_name = node.child_var.child_name.value
        semdata.symtbl[var_name].defnode.child_init.value = eval_node(node.child_expr, semdata)

    # Scalar references
    elif nodetype == 'scalar_ref':
        # If attribute has a value, return it converted to a float
        if hasattr(symtbl[node.child_name.value].defnode.child_init, "value"):
            return float(symtbl[node.child_name.value].defnode.child_init.value)

        # Otherwise evaluate nodes further
        else:
            return float(eval_node(symtbl[node.child_name.value].defnode.child_init, semdata))

    # Operators, take the left and right side and perform appropriate operation
    elif nodetype[0:4] == 'oper':
        left = eval_node(node.child_left, semdata)
        right = eval_node(node.child_right, semdata)
        oper = nodetype[5:]

        if oper == '+':
            return float(left) + float(right)
        elif oper == '-':
            return float(left) - float(right)
        elif oper == '*':
            return float(left) * float(right)
        elif oper == '/':
            return float(left) / float(right)
        elif oper == '=':
            return left == right
        elif oper == '!=':
            return left != right
        elif oper == '<':
            return left < right
        elif oper == '<=':
            return left <= right
        elif oper == '>':
            return left > right
        elif oper == '>=':
            return left >= right

    # Return a decimal value
    elif nodetype == 'decimal_number':
        return float(node.value)

    return None