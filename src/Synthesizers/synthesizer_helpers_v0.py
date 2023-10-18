from dsl import *
from exp_config import *
import copy

def bexp_hole_find_fill(bexp, goto_stmnt, stop_stmnt, cur_depth=1, depth=1):
    bexp_tps = ['and', 'or', 'neg', 'single']
    bexp_fills = []

    hole_found = False
    if bexp == None:
        hole_found = True
        if cur_depth < depth or cur_depth == 1:
            for tp in bexp_tps:
                bexp_fills = bexp_fills + bexp_hole_find_fill(Bexp(tp, None, None), goto_stmnt, stop_stmnt, cur_depth, depth)

    elif bexp.tp == None and bexp.left == None and bexp.right != None:
        hole_found = True

        bexp.tp = 'single'
        bexp_copy = copy.deepcopy(bexp)
        bexp_fills = bexp_fills + bexp_hole_find_fill(bexp_copy, goto_stmnt, stop_stmnt, cur_depth, depth)

        bexp.tp = 'neg'
        bexp_copy = copy.deepcopy(bexp)
        bexp_fills = bexp_fills + bexp_hole_find_fill(bexp_copy, goto_stmnt, stop_stmnt, cur_depth, depth)

    #TODO: Add case where can combine ors and ands

    elif bexp.tp == 'single' or bexp.tp == 'neg':
        if bexp.right == None:
            hole_found = True

            # Fill with Check Prop
            pot_check_pred = get_check_pred_fills(Check_prop(None, None), goto_stmnt, stop_stmnt)
            for check_pred in pot_check_pred:
                bexp.right = check_pred
                bexp_copy = copy.deepcopy(bexp)
                bexp_fills = bexp_fills + bexp_hole_find_fill(bexp_copy, goto_stmnt, stop_stmnt, cur_depth, depth)

            # Fill with Check Rel
            pot_check_rels = get_check_rel_fills(Check_rel(None, None, None), goto_stmnt, stop_stmnt)
            for check_rel in pot_check_rels:
                bexp.right = check_rel
                bexp_copy = copy.deepcopy(bexp)
                bexp_fills = bexp_fills + bexp_hole_find_fill(bexp_copy, goto_stmnt, stop_stmnt, cur_depth, depth)

        elif type(bexp.right) is Check_prop:
            if bexp.right.obj == None or bexp.right.obj_prop == None:
                hole_found = True
                # Fill with Check Prop
                pot_check_pred = get_check_pred_fills(bexp.right, goto_stmnt, stop_stmnt)
                for check_pred in pot_check_pred:
                    bexp.right = check_pred
                    bexp_copy = copy.deepcopy(bexp)
                    bexp_fills = bexp_fills + bexp_hole_find_fill(bexp_copy, goto_stmnt, stop_stmnt, cur_depth, depth)

        elif type(bexp.right) is Check_rel:
            if bexp.right.obj1 == None or bexp.right.obj2 == None or bexp.right.rel == None:
                hole_found = True
                # Fill with Check Rel
                pot_check_rels = get_check_rel_fills(bexp.right, goto_stmnt, stop_stmnt)
                for check_rel in pot_check_rels:
                    bexp.right = check_rel
                    bexp_copy = copy.deepcopy(bexp)
                    bexp_fills = bexp_fills + bexp_hole_find_fill(bexp_copy, goto_stmnt, stop_stmnt, cur_depth, depth)

    elif bexp.tp == 'and' or bexp.tp == 'or':
        if bexp.right == None:
            hole_found = True

            # Fill with Check Prop
            pot_check_pred = get_check_pred_fills(Check_prop(None, None), goto_stmnt, stop_stmnt)
            for check_pred in pot_check_pred:
                bexp.right = check_pred
                bexp_copy = copy.deepcopy(bexp)
                bexp_fills = bexp_fills + bexp_hole_find_fill(bexp_copy, goto_stmnt, stop_stmnt, cur_depth, depth)

                # Do Neg version
                bexp.right = Bexp('neg', right=check_pred)
                bexp_copy = copy.deepcopy(bexp)
                bexp_fills = bexp_fills + bexp_hole_find_fill(bexp_copy, goto_stmnt, stop_stmnt, cur_depth, depth)

            # Fill with Check Rel
            pot_check_rels = get_check_rel_fills(Check_rel(None, None, None), goto_stmnt,stop_stmnt)
            for check_rel in pot_check_rels:
                bexp.right = check_rel
                bexp_copy = copy.deepcopy(bexp)
                bexp_fills = bexp_fills + bexp_hole_find_fill(bexp_copy, goto_stmnt, stop_stmnt, cur_depth, depth)

                #Do Neg version
                bexp.right = Bexp('neg', right=check_rel)
                bexp_copy = copy.deepcopy(bexp)
                bexp_fills = bexp_fills + bexp_hole_find_fill(bexp_copy, goto_stmnt, stop_stmnt, cur_depth, depth)

            #If more depth possible iterate through that as well
            if cur_depth < depth:
                bexp_sub_fills = []
                for tp in bexp_tps:
                    bexp_sub_fills = bexp_sub_fills + bexp_hole_find_fill(Bexp(tp, None, None), goto_stmnt, stop_stmnt, cur_depth + 1, depth)

                for bexp_iter in bexp_sub_fills:
                    bexp.right = bexp_iter
                    bexp_copy = copy.deepcopy(bexp)
                    bexp_fills = bexp_fills + bexp_hole_find_fill(bexp_copy, goto_stmnt, stop_stmnt, cur_depth, depth)

        elif type(bexp.right) is Check_prop_pred:
            if bexp.right.obj == None or bexp.right.obj_prop == None:
                hole_found = True
                # Fill with Check Prop
                pot_check_pred = get_check_pred_fills(bexp.right, goto_stmnt, stop_stmnt)
                for check_pred in pot_check_pred:
                    bexp.right = check_pred
                    bexp_copy = copy.deepcopy(bexp)
                    bexp_fills = bexp_fills + bexp_hole_find_fill(bexp_copy, goto_stmnt, stop_stmnt, cur_depth, depth)

        elif type(bexp.right) is Check_rel_pred:
            if bexp.right.obj1 == None or bexp.right.obj2 == None or bexp.right.rel == None:
                hole_found = True
                # Fill with Check Rel
                pot_check_rels = get_check_rel_fills(bexp.right, goto_stmnt, stop_stmnt)
                for check_rel in pot_check_rels:
                    bexp.right = check_rel
                    bexp_copy = copy.deepcopy(bexp)
                    bexp_fills = bexp_fills + bexp_hole_find_fill(bexp_copy, goto_stmnt, stop_stmnt, cur_depth, depth)

        if bexp.left == None:
            hole_found = True

            # Fill with Check Prop
            pot_check_pred = get_check_pred_fills(Check_prop(None, None), goto_stmnt, stop_stmnt)
            for check_pred in pot_check_pred:
                bexp.left = check_pred
                bexp_copy = copy.deepcopy(bexp)
                bexp_fills = bexp_fills + bexp_hole_find_fill(bexp_copy, goto_stmnt, stop_stmnt, cur_depth, depth)

                # Do Neg version
                bexp.left = Bexp('neg', right=check_pred)
                bexp_copy = copy.deepcopy(bexp)
                bexp_fills = bexp_fills + bexp_hole_find_fill(bexp_copy, goto_stmnt, stop_stmnt, cur_depth, depth)

            # Fill with Check Rel
            pot_check_rels = get_check_rel_fills(Check_rel(None, None, None), goto_stmnt, stop_stmnt)
            for check_rel in pot_check_rels:
                bexp.left = check_rel
                bexp_copy = copy.deepcopy(bexp)
                bexp_fills = bexp_fills + bexp_hole_find_fill(bexp_copy, goto_stmnt, stop_stmnt, cur_depth, depth)

                # Do Neg version
                bexp.left = Bexp('neg', right=check_rel)
                bexp_copy = copy.deepcopy(bexp)
                bexp_fills = bexp_fills + bexp_hole_find_fill(bexp_copy, goto_stmnt, stop_stmnt, cur_depth, depth)

            # If more depth possible iterate through that as well
            if cur_depth < depth:
                bexp_sub_fills = []
                for tp in bexp_tps:
                    bexp_sub_fills = bexp_sub_fills + bexp_hole_find_fill(Bexp(tp, None, None), goto_stmnt, stop_stmnt, cur_depth, depth)

                for bexp_iter in bexp_sub_fills:
                    bexp.left = bexp_iter
                    bexp_copy = copy.deepcopy(bexp)
                    bexp_fills = bexp_fills + bexp_hole_find_fill(bexp_copy, goto_stmnt, stop_stmnt, cur_depth + 1, depth)

        elif type(bexp.left) is Check_prop:
            if bexp.left.obj == None or bexp.left.obj_prop == None:
                # Fill with Check Prop
                pot_check_pred = get_check_pred_fills(bexp.left, goto_stmnt, stop_stmnt)
                for check_pred in pot_check_pred:
                    bexp.left = check_pred
                    bexp_copy = copy.deepcopy(bexp)
                    bexp_fills = bexp_fills + bexp_hole_find_fill(bexp_copy, goto_stmnt, stop_stmnt, cur_depth, depth)

        elif type(bexp.left) is Check_rel_pred:
            if bexp.left.obj1 == None or bexp.left.obj2 == None or bexp.left.rel == None:
                # Fill with Check Rel
                pot_check_rels = get_check_rel_fills(bexp.left, goto_stmnt, stop_stmnt)
                for check_rel in pot_check_rels:
                    bexp.left = check_rel
                    bexp_copy = copy.deepcopy(bexp)
                    bexp_fills = bexp_fills + bexp_hole_find_fill(bexp_copy, goto_stmnt, stop_stmnt, cur_depth, depth)


    if not hole_found:
        bexp_fills.append(bexp)

    return bexp_fills



def fill_holed_bexp(missing, tp):
    """
    Fills left/right holes in Bexps with check_props or check_rels
    :param missing: What part of the bexp is missing
    :return: List of potential fills for the type of hole (left, right)
    """

    fills = []

    #This case is open to all combinations
    hole_check_prop_1 = Check_prop(None, None)
    hole_check_prop_2 = Check_prop(None, None)
    hole_check_rel_1 = Check_rel(None, None, None)
    hole_check_rel_2 = Check_rel(None, None, None)
    if missing == 'Right' and tp == 'neg':
        fills.append((None, hole_check_prop_1))
        fills.append((None, hole_check_rel_1))
    else:
        fills.append((hole_check_prop_1, hole_check_prop_2))
        fills.append((hole_check_prop_1, hole_check_rel_1))

        fills.append((hole_check_rel_1, hole_check_rel_2))

    return fills

def get_object_set(goto_stmt, stmnt, return_types=False):
    possible_object_sets = []
    for stmnt_iter in goto_stmt.statements:
        if id(stmnt) == id(stmnt_iter):
            break

        #Check if stmnt_iter is a scan, if so append it's object_set
        if type(stmnt_iter) is Scan:
            if return_types:
                possible_object_sets.append((stmnt_iter.obj_set, stmnt_iter.obj_tp))
            else:
                possible_object_sets.append(stmnt_iter.obj_set)

    return possible_object_sets

def get_valid_obj_tps(stmnt):
    obj_tps = []
    for sub_stmnt in stmnt.statements:
        if type(sub_stmnt) is If:
            obj_tps += get_valid_obj_tps(sub_stmnt)
        if type(sub_stmnt) is Act:
            obj_tps.append(sub_stmnt.obj_tp)

    return obj_tps

def get_objects(goto_stmt, stmnt):
    possible_object = []
    for stmnt_iter in goto_stmt.statements:
        if id(stmnt) == id(stmnt_iter):
            break

        # Check if stmnt_iter is a scan, if so append it's object
        if type(stmnt_iter) is Let:
            possible_object.append(stmnt_iter.v)

        #Check if stmnt_iter is for each, if so get it's object iterator
        if type(stmnt_iter) is Foreach_obj:
            possible_object.append(stmnt_iter.itr)

    return possible_object

def get_objects_w_types(goto_stmt, stmnt):
    possible_object = []
    for stmnt_iter in goto_stmt.statements:
        if id(stmnt) == id(stmnt_iter):
            break

        # Check if stmnt_iter is a scan, if so append it's object
        if type(stmnt_iter) is Let:
            possible_object.append((stmnt_iter.v, get_types(goto_stmt, stmnt, stmnt_iter.v)))

        #Check if stmnt_iter is for each, if so get it's object iterator
        if type(stmnt_iter) is Foreach_obj:
            possible_object.append((stmnt_iter.itr, get_types(goto_stmt, stmnt, stmnt_iter.itr)))

    return possible_object

def get_types(goto_stmt, stmnt, obj):
    pot_object_sets_and_types = []
    for stmnt_iter in goto_stmt.statements:
        if id(stmnt) == id(stmnt_iter):
            break

        # Check if stmnt_iter is a scan, if so append to the object sets to check
        if type(stmnt_iter) is Scan:
            pot_object_sets_and_types.append((stmnt_iter.obj_set, stmnt_iter.obj_tp))

    #Use the object sets found to get object types matching variable in foreach and let
    pot_object_types = []
    for stmnt_iter in goto_stmt.statements:
        if id(stmnt) == id(stmnt_iter):
            break
        #Check let statements
        if type(stmnt_iter) is Let and stmnt_iter.v.id == obj.id:
            #Find in object_sets and types list
            for (obj_set, obj_tp) in pot_object_sets_and_types:
                if stmnt_iter.v_bar != None and obj_set.id == stmnt_iter.v_bar.id:
                    pot_object_types.append(obj_tp)

        if type(stmnt_iter) is Foreach_obj and stmnt_iter.itr.id == obj.id:
            # Find in object_sets and types list
            for (obj_set, obj_tp) in pot_object_sets_and_types:
                if stmnt_iter.obj_set != None and obj_set.id == stmnt_iter.obj_set.id:
                    pot_object_types.append(obj_tp)

    return pot_object_types

def get_check_rel_fills(check_rel, goto_stmnt, stop_stmnt):
    pot_obj_1 = []
    if check_rel.obj1 == None:
        pot_obj_1 = pot_obj_1 + get_objects(goto_stmnt, stop_stmnt)
    else:
        pot_obj_1.append(check_rel.obj1)

    pot_obj_2 = []
    if check_rel.obj2 == None:
        pot_obj_2 = get_objects(goto_stmnt, stop_stmnt)
    else:
        pot_obj_2.append(check_rel.obj2)

    pot_rel = []
    if check_rel.rel == None:
        for rel in env_def.relations:
            pot_rel.append(rel)
    else:
        pot_rel = pot_rel.append(check_rel.rel)

    filled_check_rels = []
    for obj1 in pot_obj_1:
        for obj2 in pot_obj_2:
            for rel in pot_rel:
                filled_check_rels.append(Check_rel(obj1, obj2, rel))

    return filled_check_rels

def get_check_pred_fills(check_pred, goto_stmnt, stop_stmnt):
    pot_objs = []
    if check_pred.obj == None:
        pot_objs = pot_objs + get_objects(goto_stmnt, stop_stmnt)
    else:
        pot_objs.append(check_pred.obj)

    check_pred_fills = []
    if check_pred.obj_prop == None:
        for obj in pot_objs:
            object_types = get_types(goto_stmnt, stop_stmnt, obj)

            for tp in object_types:
                for prop in env_def.properties[tp]:
                    check_pred_fills.append(Check_prop(obj, prop))

    else:
        for obj in pot_objs:
            check_pred_fills.append(Check_prop(obj, check_pred.obj_prop))

    return check_pred_fills

def get_all_objects(sketch):
    object_iterators = []
    for s_stmnt in sketch:
        if type(s_stmnt) is Goto:
            object_iterators = object_iterators + get_all_objects(s_stmnt.statements)

        if type(s_stmnt) is Let:
            object_iterators.append(s_stmnt.v)

        if type(s_stmnt) is Foreach_obj:
            object_iterators.append(variable(s_stmnt.itr.pretty_str(0)))

            object_iterators = object_iterators + get_all_objects(s_stmnt.statements)

        if type(s_stmnt) is If:
            object_iterators = object_iterators + get_all_objects(s_stmnt.statements)

    return object_iterators
