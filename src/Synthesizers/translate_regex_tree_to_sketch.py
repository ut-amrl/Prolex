from dsl import *

def translate_regex_tree_to_sub_sketch(regex_node, let_tps, scan_tps):
    sub_statements = []
    if regex_node.tp == "star" or regex_node.tp == "plus":
        #Sub sketch is gotoeach
        if len(regex_node.sub_tree) == 1 and len(regex_node.sub_tree[0].sub_tree) > 0 and\
                "goto" in regex_node.sub_tree[0].sub_tree[0].tp:
            i = Iterator()
            sub_statement = Goto('Goto_each', itr=i)

            #Iterate subtree
            goto_sub_statements = []
            for sub_regex_node in regex_node.sub_tree[0].sub_tree[1::]: #Dont want to include goto
                temp_sub_statements = translate_regex_tree_to_sub_sketch(sub_regex_node, let_tps, deepcopy(scan_tps))
                if temp_sub_statements == None:
                    return None

                goto_sub_statements += temp_sub_statements

            sub_statement.statements = goto_sub_statements

            sub_statements.append(sub_statement)
            return sub_statements

        #Sub sketch is foreach
        else:
            i = Iterator()
            sub_statement = Foreach_obj(i, None)

            #Iterate subtree
            foreach_sub_statements = []
            before_foreach_statements = []
            for sub_regex_node in regex_node.sub_tree:
                temp_sub_stmnts = translate_regex_tree_to_sub_sketch(sub_regex_node, let_tps, scan_tps)

                if temp_sub_stmnts == None:
                    return None

                for sub_stmnt in temp_sub_stmnts:
                    #Don't put in foreach if there is an associated let
                    #Don't put lets in foreach
                    if type(sub_stmnt) is Let:
                        before_foreach_statements.append(sub_stmnt)
                    elif type(sub_stmnt) is Scan:
                        before_foreach_statements.append(sub_stmnt)
                    elif type(sub_stmnt) is Act and sub_stmnt.obj_tp in let_tps:
                        for reps in range(let_tps[sub_stmnt.obj_tp]):
                            # Check if scan needed
                            if type(sub_stmnt) is Act and sub_stmnt.obj_tp not in scan_tps:
                                os = object_set()
                                scan_stmnt = Scan(sub_stmnt.obj_tp, os)
                                before_foreach_statements.append(scan_stmnt)

                                scan_tps[sub_stmnt.obj_tp] = True

                            # Make if
                            if_statement = If(None)
                            if_statement.statements.append(deepcopy(sub_stmnt))

                            before_foreach_statements.append(if_statement)
                    else:
                        #Check if scan needed
                        if type(sub_stmnt) is Act and sub_stmnt.obj_tp not in scan_tps:
                            os = object_set()
                            scan_stmnt = Scan(sub_stmnt.obj_tp, os)
                            before_foreach_statements.append(scan_stmnt)

                            scan_tps[sub_stmnt.obj_tp] = True

                        # Make if
                        if_statement = If(None)
                        if_statement.statements.append(sub_stmnt)

                        foreach_sub_statements.append(if_statement)

            sub_statement.statements = foreach_sub_statements

            sub_statements += before_foreach_statements

            if len(foreach_sub_statements) > 0:
                sub_statements.append(sub_statement)

            return sub_statements

    elif regex_node.tp == "concat":
        if 'goto' in regex_node.sub_tree[0].tp:
            sub_statement = Goto('Goto', None)

            # Iterate subtree
            goto_sub_statements = []
            for sub_regex_node in regex_node.sub_tree[1::]:  # Dont want to include goto
                temp_sub_statements = translate_regex_tree_to_sub_sketch(sub_regex_node, let_tps, scan_tps)

                if temp_sub_statements == None:
                    return None

                goto_sub_statements += temp_sub_statements

            sub_statement.statements = goto_sub_statements

            sub_statements.append(sub_statement)
            return sub_statements
        else:
            # Iterate subtree
            concat_sub_statements = []
            for sub_regex_node in regex_node.sub_tree:  # Dont want to include goto
                temp_sub_statements = translate_regex_tree_to_sub_sketch(sub_regex_node, let_tps, scan_tps)

                if temp_sub_statements == None:
                    return None

                concat_sub_statements += temp_sub_statements

            sub_statements += concat_sub_statements

            return sub_statements

    elif regex_node.tp == "?":
        sub_statement = If(None)

        # Iterate subtree
        if_sub_statements = []
        for sub_regex_node in regex_node.sub_tree:
            temp_sub_stmnts = translate_regex_tree_to_sub_sketch(sub_regex_node, let_tps, scan_tps)

            if temp_sub_stmnts == None:
                return None

            for sub_stmnt in temp_sub_stmnts:
                if_sub_statements.append(sub_stmnt)

        sub_statement.statements = if_sub_statements

        sub_statements.append(sub_statement)

        return sub_statements

    elif 'let' in regex_node.tp:  # Let
        # Parse
        split = regex_node.tp.split('_')
        num_required = int(split[-1])
        obj_tp = None

        for i in range(len(split)):
            if i == 1 and split[i] != 'QMark':
                obj_tp = split[i]

        let_tps[obj_tp] = num_required

        #Create scan for new variable type
        os = object_set()
        sub_statement = Scan(obj_tp, os)
        sub_statements.append(sub_statement)
        scan_tps[obj_tp] = True

        # Create variable for let (1 for each required)
        for i in range(num_required):
            v = variable(None)
            sub_statement = Let(v, None, None, obj_tp, inst=i)

            sub_statements.append(sub_statement)

        return sub_statements

    elif 'act' in regex_node.tp: #Act
        #Parse
        split = regex_node.tp.split('_')
        obj_tp = None
        action = None
        rel_set = []

        for i in range(len(split)):
            if i == 1 and split[i] != 'QMark':
                obj_tp = split[i]
            if i == 2 and split[i] != 'QMark':
                action = split[i]
            if i == 3 and split[i] != 'QMark':
                rel_set = [(split[i], None)]

        sub_statement = Act(None, action, obj_tp, rel_set)

        sub_statements.append(sub_statement)

        return sub_statements

    else: #Invalid, all other types should be consumed before this
        #Sometimes regex produces concats with check prop in it -- can just ignore
        return None