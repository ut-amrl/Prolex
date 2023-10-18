from demo import *
from Synthesizers.Defs.XML_Node import *
import copy

def demo_to_xml_node_top(statements):
    lets_required = get_num_lets_required(statements)

    list_of_xml_node_lists = []
    for lets_dict in lets_required:
        lets_generated = {}
        for obj in lets_dict:
            lets_generated[obj] = 0

        xml_node_list = demo_to_xml_node(statements, lets_dict, lets_generated)

        list_of_xml_node_lists.append(xml_node_list)

    return list_of_xml_node_lists

def demo_to_xml_node(statements, required_lets, lets_generated, goto_depth=1, scan_depth=1):
    goto_breadth = 0

    node_list = []

    #Loop through statements
    iterations = 0
    prev_sub_node_type = None
    for stmnt in statements:
        iterations = iterations + 1
        #Check statement type
        if type(stmnt) is Goto_stmnt:
            sub_nodes = demo_to_xml_node(
                stmnt.statements, required_lets, deepcopy(lets_generated), goto_depth + goto_breadth + 1, scan_depth)

            is_return_goto = False
            if len(sub_nodes) > 0:
                if sub_nodes[0].tp.find('let') == -1:
                    tp_chk = sub_nodes[0].tp
                else:
                    tp_chk = sub_nodes[1].tp
                if prev_sub_node_type != tp_chk and (goto_depth > 1 or prev_sub_node_type != None):
                    goto_breadth = goto_breadth + 1

                if sub_nodes[0].tp.find('let') == -1:
                    prev_sub_node_type = sub_nodes[0].tp
                else:
                    prev_sub_node_type = sub_nodes[1].tp
            else:
                goto_breadth += 1
            # else:
            #     goto_breadth = goto_breadth - 1
            #     prev_sub_node_type = None
            #
            #     is_return_goto = True

            #Redo with proper goto_breadth
            sub_nodes = demo_to_xml_node(
                stmnt.statements, required_lets, deepcopy(lets_generated), goto_depth + goto_breadth, scan_depth)

            if is_return_goto:
                # xml_type = "goto_r"
                xml_type = "goto" + str(goto_depth + goto_breadth)
            else:
                xml_type = "goto" + str(goto_depth + goto_breadth)
            xml_node = XML_Node(xml_type)

            xml_node.sub_nodes = sub_nodes

            node_list.append(xml_node)

        elif type(stmnt) is Act_stmnt:
            act_type = "_" + stmnt.action

            obj_tps = []
            obj_tp = "_QMark"
            if stmnt.obj_name != "?":
                obj_tp = "_" + stmnt.obj.split("_")[0]
                obj_tps.append(obj_tp.removeprefix("_"))

            rel_set = ''
            if stmnt.action == 'Place':
                for rel in stmnt.rel_set:
                    rel_set = rel_set + "_" + rel[0] + "_" + rel[1]
                    obj_tps.append(rel[1].split('_')[0])

            # Check if let insertion required
            found_obj_tp = []
            for curr_obj_tp in obj_tps:
                if curr_obj_tp in required_lets and (
                        required_lets[curr_obj_tp] - lets_generated[curr_obj_tp]) > 0 and curr_obj_tp not in found_obj_tp:
                    found_obj_tp.append(curr_obj_tp)

            # Generate Lets if any
            if len(found_obj_tp) > 0:
                for curr_obj_tp in found_obj_tp:
                    xml_type = "let" + "_" + curr_obj_tp + "_req_" + str(required_lets[curr_obj_tp])
                    let_node = XML_Node(xml_type)

                    #Don't need to worry about subnoding anymore
                    node_list.append(let_node)

                    lets_generated[curr_obj_tp] = required_lets[curr_obj_tp]

                xml_type = "act" + obj_tp + act_type + rel_set
                xml_node = XML_Node(xml_type)

                # Don't need to worry about subnoding anymore
                node_list.append(xml_node)

                sub_nodes = demo_to_xml_node(
                    statements[iterations::], required_lets, deepcopy(lets_generated),
                    goto_depth + goto_breadth,
                    scan_depth)

                node_list = node_list + sub_nodes

                break

            else:
                xml_type = "act" + obj_tp + act_type + rel_set
                xml_node = XML_Node(xml_type)

                node_list.append(xml_node)

    return node_list

def check_for_let_insertion(statements, obj_tp):
    #Check number of occurences of obj_tp per loc
    num_occ = -1
    curr_num_occ = 0
    for goto in statements:
        curr_num_occ = get_num_occ(goto.statements, obj_tp)

        if num_occ == -1:
            num_occ = curr_num_occ
            first_goto_sub_stmnt = str(type(goto.statements[0])) + str(goto.statements[0].action)

        #Need to check if goto outside gotoeach
        if (goto.statements == [] or (curr_num_occ != num_occ and
                (str(type(goto.statements[0])) + str(goto.statements[0].action)) == first_goto_sub_stmnt)):
            return 0

    if num_occ > curr_num_occ:
        return num_occ
    else:
        return curr_num_occ


def get_num_occ(goto_stmnt, obj_tp):
    curr_num_occ = 0
    objs_seen = set()
    for stmnt in goto_stmnt:
        if type(stmnt) is Goto_stmnt:
            continue #TODO: I think this is fine to skip. Most sub-gotos involve objs robot is holding

        if type(stmnt) is Act_stmnt:
            if stmnt.obj_name != "?":
                cur_obj_tp = stmnt.obj_name.split("_")[0]

                if obj_tp == cur_obj_tp and stmnt.obj_name not in objs_seen:
                    objs_seen.add(stmnt.obj_name)
                    curr_num_occ = curr_num_occ + 1

            #Check rel set
            for rel in stmnt.rel_set:
                cur_obj_tp = rel[1].split("_")[0]

                if obj_tp == cur_obj_tp and rel[1] not in objs_seen:
                    objs_seen.add(rel[1])
                    curr_num_occ = curr_num_occ + 1

    return curr_num_occ

def get_num_lets_required(demo_statements):
    #Create set of observed objects
    obj_tps = set()
    for goto in demo_statements:
        for stmnt in goto.statements:
            if type(stmnt) is Act_stmnt:
                if stmnt.obj_name != "?":
                    cur_obj_tp = stmnt.obj_name.split("_")[0]
                    obj_tps.add(cur_obj_tp)

                # Check rel set
                for rel in stmnt.rel_set:
                    cur_obj_tp = rel[1].split("_")[0]
                    obj_tps.add(cur_obj_tp)

    lets_required = {}
    for obj_tp in obj_tps:
        lets_required[obj_tp] = check_for_let_insertion(demo_statements, obj_tp)

    return cartesian_product_of_lets(lets_required)

def cartesian_product_of_lets(lets_required):
    prod_set = [{}]
    if len(lets_required) == 1:
        prod_set.append(lets_required)
        return prod_set

    if len(lets_required) == 0:
        return []

    lets_required_cp = deepcopy(lets_required)
    for obj in lets_required:
        val = lets_required_cp.pop(obj)

        sub_sets = cartesian_product_of_lets(deepcopy(lets_required_cp))

        if not check_in_prod_set(deepcopy({obj: val}), prod_set):
            prod_set.append(deepcopy({obj: val}))

        for sub in sub_sets:
            if not check_in_prod_set(sub, prod_set):
                prod_set.append(deepcopy(sub))

            sub[obj] = val
            if not check_in_prod_set(sub, prod_set):
                prod_set.append(sub)

    return prod_set

def check_in_prod_set(sub, prod_set):
    for obj_dict in prod_set:
        shared_items = {k: obj_dict[k] for k in obj_dict if k in sub and obj_dict[k] == sub[k]}

        if len(shared_items) == len(sub):
            return True

    return False