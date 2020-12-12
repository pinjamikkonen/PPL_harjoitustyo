# Pinja Mikkonen 99219
# Priciples of Programming Languages
# Project Work - Phase 4

def run_program(tree, semdata):
    semdata.stack = []
    eval_node(tree, semdata)

def eval_node(node, semdata):
    symtbl = semdata.symtbl
    nodetype = node.nodetype

    if nodetype == 'program':
#        for i in node.children_funcs_vars:
#            eval_node(i, semdata)
        for i in node.children_stmt_list:
            eval_node(i, semdata)
        return None

    if nodetype == 'function_def':
        for i in node.children_stmt_list:
            eval_node(i, semdata)

    if nodetype == 'function_call':
        eval_node(symtbl[node.child_name.value].defnode, semdata)
        return None

    if nodetype == 'subroutine_def':
        for i in node.children_stmts:
            eval_node(i, semdata)

    if nodetype == 'subroutine_call':
        eval_node(symtbl[node.child_name.value].defnode, semdata)
        return None

    if nodetype == 'if_stmt':
        if eval_node(symtbl[node.child_cond].defnode, semdata):
            for i in node.children_then_list:
                eval_node(i, semdata)

    if nodetype == 'print_scalar':
        print(eval_node(node.child_expr, semdata))
        return None

    if nodetype == 'scalar_ref':
        return symtbl[node.child_name.value].defnode.child_init.value

    if nodetype[0:4] == 'oper':
        left = eval_node(node.child_left, semdata)
        right = eval_node(node.child_right, semdata)
        oper = nodetype[5:]
        print(oper)

        if oper == '+':
            return left + right
        elif oper == '-':
            return left - right
        elif oper == '*':
            return left * right
        elif oper == '/':
            return left / right
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
        else:
            print("Nyt tapahtui jotain outoa D:")


    if nodetype == 'decimal_number':
        return float(node.value)

    return None