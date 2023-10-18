from dsl import *

def fill_hole(sketch, hole_stmnt_pos, hole_idx, fill):
    stmnt = sketch
    for pos in hole_stmnt_pos:
        stmnt = stmnt.statements[pos]

    if type(stmnt) is Goto:
        stmnt.loc = variable(fill)
        #stmnt.loc = fill

        return sketch

    if type(stmnt) is Scan:
        stmnt.obj_tp = fill

        return sketch

    if type(stmnt) is Let:
        # Default Ordering
        if hole_idx == 0:
            stmnt.v_bar = fill

            return sketch

        if hole_idx == 1:
            stmnt.i = fill

            return sketch

    if type(stmnt) is If:
        if hole_idx == 0:
            # Whole if is hole
            if stmnt.bexp == None:
                stmnt.bexp = fill
            else:
                stmnt.bexp.tp = fill

            return sketch

        if hole_idx == 1:
            if stmnt.bexp.left == None:
                stmnt.bexp.left = fill
                return sketch

            if type(stmnt.bexp.left) is Check_prop:
                if stmnt.bexp.left.obj == None:
                    stmnt.bexp.left.obj = fill
                    return sketch

                if stmnt.bexp.left.obj_prop == None:
                    stmnt.bexp.left.obj_prop = fill
                    return sketch

            if type(stmnt.bexp.left) is Check_rel:
                if stmnt.bexp.left.obj1 == None:
                    stmnt.bexp.left.obj1 = fill
                    return sketch

                if stmnt.bexp.left.obj2 == None:
                    stmnt.bexp.left.obj2 = fill
                    return sketch

                if stmnt.bexp.left.rel == None:
                    stmnt.bexp.left.rel = fill
                    return sketch

        if hole_idx == 2:
            if stmnt.bexp.right == None:
                stmnt.bexp.right = fill
                return sketch

            if type(stmnt.bexp.right) is Check_prop:
                if stmnt.bexp.right.obj == None:
                    stmnt.bexp.right.obj = fill
                    return sketch

                if stmnt.bexp.right.obj_prop == None:
                    stmnt.bexp.right.obj_prop = fill
                    return sketch

            if type(stmnt.bexp.right) is Check_rel:
                if stmnt.bexp.right.obj1 == None:
                    stmnt.bexp.right.obj1 = fill
                    return sketch

                if stmnt.bexp.right.obj2 == None:
                    stmnt.bexp.right.obj2 = fill
                    return sketch

                if stmnt.bexp.right.rel == None:
                    stmnt.bexp.right.rel = fill
                    return sketch

    if type(stmnt) is Foreach_obj:
        stmnt.obj_set = fill
        return sketch

    if type(stmnt) is Act:
        if hole_idx == 0:
            stmnt.obj = fill
            return sketch

        if hole_idx == 1:
            if stmnt.rel_set == []:
                stmnt.rel_set = fill
                return sketch
            else:
                #Find first with None object
                for i in range(len(stmnt.rel_set)):
                    if stmnt.rel_set[i][1] == None:
                        stmnt.rel_set[i] = [stmnt.rel_set[i][0], fill]

                        break

                return sketch