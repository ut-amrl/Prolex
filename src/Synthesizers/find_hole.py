from dsl import *
import copy
from Synthesizers.ordered_hole_fills_w_prob import ordered_hole_fills_w_prob
from Synthesizers.fill_holes import fill_hole

def find_hole(top, search_method="Preorder"):
    if search_method == "Preorder":
        stmnt_depth = []
        stmnt_count = 0
        for stmnt in top.statements:
            if type(stmnt) is Goto:
                if stmnt.tp == "Goto" and stmnt.loc == None:
                    stmnt_depth.append(stmnt_count)
                    return stmnt_depth, 0
                elif len(stmnt.statements) > 0:
                    #Check substatements
                    hole_stmnt_pos, hole_idx = find_hole(stmnt, search_method)

                    if hole_stmnt_pos != None:
                        stmnt_depth.append(stmnt_count)
                        stmnt_depth = stmnt_depth + hole_stmnt_pos
                        return stmnt_depth, hole_idx

            if type(stmnt) is Scan and stmnt.obj_tp == None:
                stmnt_depth.append(stmnt_count)
                return stmnt_depth, 0

            if type(stmnt) is Let:
                if stmnt.v_bar == None:
                    stmnt_depth.append(stmnt_count)
                    return stmnt_depth, 0
                if stmnt.i == None:
                    stmnt_depth.append(stmnt_count)
                    return stmnt_depth, 1

            if type(stmnt) is If:
                if stmnt.bexp == None or stmnt.bexp.tp == None:
                    stmnt_depth.append(stmnt_count)
                    return stmnt_depth, 0
                elif stmnt.bexp.tp == 'and' or stmnt.bexp.tp == 'or':
                        if stmnt.bexp.right == None:
                            stmnt_depth.append(stmnt_count)
                            return stmnt_depth, 2
                        if stmnt.bexp.left == None:
                            stmnt_depth.append(stmnt_count)
                            return stmnt_depth, 1
                elif (stmnt.bexp.tp == 'neg' or stmnt.bexp.tp == 'single') and stmnt.bexp.right == None:
                    stmnt_depth.append(stmnt_count)
                    return stmnt_depth, 2

                if stmnt.bexp.tp != 'True' and stmnt.bexp.tp != 'False': #One of the checks might have a hole still
                    if ((type(stmnt.bexp.left) is Check_prop and (
                        stmnt.bexp.left.obj == None or
                        stmnt.bexp.left.obj_prop == None)) or (type(stmnt.bexp.left) is Check_rel and (
                        stmnt.bexp.left.obj1 == None or
                        stmnt.bexp.left.obj2 == None or
                        stmnt.bexp.left.rel == None))):

                        stmnt_depth.append(stmnt_count)
                        return stmnt_depth, 1

                    if ((type(stmnt.bexp.right) is Check_prop and (
                            stmnt.bexp.right.obj == None or
                            stmnt.bexp.right.obj_prop == None)) or (type(stmnt.bexp.right) is Check_rel and (
                            stmnt.bexp.right.obj1 == None or
                            stmnt.bexp.right.obj2 == None or
                            stmnt.bexp.right.rel == None))):
                        stmnt_depth.append(stmnt_count)
                        return stmnt_depth, 2

                #Check sub statements
                hole_stmnt_pos, hole_idx = find_hole(stmnt, search_method)

                if hole_stmnt_pos != None:
                    stmnt_depth.append(stmnt_count)
                    stmnt_depth = stmnt_depth + hole_stmnt_pos
                    return stmnt_depth, hole_idx

            if type(stmnt) is Foreach_obj:
                if stmnt.obj_set == None:
                    stmnt_depth.append(stmnt_count)
                    return stmnt_depth, 0

                # Check sub statements
                hole_stmnt_pos, hole_idx = find_hole(stmnt, search_method)

                if hole_stmnt_pos != None:
                    stmnt_depth.append(stmnt_count)
                    stmnt_depth = stmnt_depth + hole_stmnt_pos
                    return stmnt_depth, hole_idx

            if type(stmnt) is Act:
                if stmnt.obj == None:
                    stmnt_depth.append(stmnt_count)
                    return stmnt_depth, 0

                missing_object = False

                for rel in stmnt.rel_set:
                    if rel[1] == None:
                        missing_object = True

                if stmnt.action == 'Place' and (stmnt.rel_set == None or
                        missing_object):
                    stmnt_depth.append(stmnt_count)
                    return stmnt_depth, 1

            stmnt_count = stmnt_count + 1

        return None, 0

def find_hole_best_hole(sketch, LM, env, demo, tp, lm_lock):
    temp_sketch = deepcopy(sketch)

    #Find all holes
    temp_hole_pos, temp_hole_idx = find_hole(temp_sketch)
    best_prediction = -1
    best_hole_pos = None
    best_hole_idx = 0
    while temp_hole_pos != None:
        #Get hole_fill from LLM using actual sketch
        hole_fills_sorted, filled_by_LLM = ordered_hole_fills_w_prob(LM.LM, sketch, env, temp_hole_pos, temp_hole_idx, demo, tp, lm_lock)

        if hole_fills_sorted == []:
            #print("FAILED: ", best_prediction, best_hole_pos, best_hole_idx)
            #print("CHECKED: ", temp_hole_pos, temp_hole_idx)
            
            break

        cur_best_pred, cur_fill = hole_fills_sorted[0]

        if filled_by_LLM and cur_best_pred > best_prediction:
            best_prediction = cur_best_pred
            best_hole_pos = temp_hole_pos
            best_hole_idx = temp_hole_idx
        elif best_prediction == -1 and best_hole_pos == None:
            best_hole_pos = temp_hole_pos
            best_hole_idx = temp_hole_idx

        #Fill temp_sketch hole then get next hole location
        if type(cur_fill) is not Bexp:
            temp_sketch = fill_hole(deepcopy(temp_sketch), temp_hole_pos, temp_hole_idx, cur_fill)
        else:
            temp_sketch = fill_hole(deepcopy(temp_sketch), temp_hole_pos, temp_hole_idx, Bexp('True', None, None))
            
        temp_hole_pos, temp_hole_idx = find_hole(temp_sketch)

    

    #print("Finding FUNC:", best_hole_pos, best_hole_idx)

    #If best hole is None possible hangup in LLM filler (trying to get an action but object set not set)
    #Just return regular hole fill
    if best_hole_pos == None:
        return find_hole(sketch)

    return best_hole_pos, best_hole_idx
