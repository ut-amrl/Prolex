from Synthesizers.synthesizer_helpers_v0 import *
#from Env import env_def
import copy
from dsl import *

def ennumerator_v0(env, skeleton):
    """
    Simple ennumerative search over the holes in a skeleton program
    :param env: The current environment that we are generating a program for
    :param skeleton: A program with holes
    :return: A set of complete programs
    """

    completed_progs = []

    #Iterate through Goto statements

    goto_iter_count = 0
    hole_found = False
    for goto_stmt in skeleton.statements:
        #Single goto statement rather than foreach
        if goto_stmt.tp == 'Goto' and goto_stmt.loc == None:
            hole_found = True
            for loc in env.locations:
                #Fill goto stmnt with loc
                goto_stmt.loc = variable(loc)

                #Recurse
                skeleton_cpy = copy.deepcopy(skeleton)
                goto_stmt_cpy = skeleton_cpy.statements[goto_iter_count]
                completed_progs = completed_progs + sub_statement_ennumerator_v0(env, skeleton_cpy, goto_stmt_cpy, goto_stmt_cpy, goto_iter_count)

        elif goto_stmt.tp == 'Goto_each':
            hole_found = True

            # Recurse
            skeleton_cpy = copy.deepcopy(skeleton)
            goto_stmt_cpy = skeleton_cpy.statements[goto_iter_count]
            completed_progs = completed_progs + sub_statement_ennumerator_v0(env, skeleton_cpy, goto_stmt_cpy,
                                                                             goto_stmt_cpy, goto_iter_count)


        if not hole_found:
            skeleton_cpy = copy.deepcopy(skeleton)
            goto_stmt_cpy = skeleton_cpy.statements[goto_iter_count]
            completed_progs = completed_progs + sub_statement_ennumerator_v0(env, skeleton_cpy, goto_stmt_cpy, goto_stmt_cpy, goto_iter_count)

        goto_iter_count = goto_iter_count + 1

    return completed_progs


def sub_statement_ennumerator_v0(env, skeleton, goto_stmt, top_level_stmnt, goto_iter_count, stmt_depth=[]):
    completed_progs = []

    hole_found = False

    stmt_iter_count = 0

    for stmnt in top_level_stmnt.statements:
        if type(stmnt) is Goto and stmnt.tp == 'Goto' and stmnt.loc == None:
            hole_found = True
            for loc in env.locations:
                #Fill goto stmnt with loc
                stmnt.loc = variable(loc)

                if len(stmnt.statements) > 0:
                    hole_found = True  # Not necessarily a hole but fills will be found in recursion
                    # Ennumerate sub statements
                    skeleton_cpy = copy.deepcopy(skeleton)
                    goto_stmt_cpy = skeleton_cpy.statements[goto_iter_count]

                    # Fix sub statements
                    stmt_depth.append(stmt_iter_count)
                    stmnt_cpy = skeleton_cpy.statements[goto_iter_count]

                    for i in stmt_depth:
                        stmnt_cpy = stmnt_cpy.statements[i]

                    completed_progs = completed_progs + sub_statement_ennumerator_v0(
                        env, skeleton_cpy, goto_stmt_cpy, stmnt_cpy, goto_iter_count, stmt_depth)


                    stmt_depth.pop(-1)

            # Rest of recursion handled above
            break

        if type(stmnt) is Goto and stmnt.tp == 'Goto_each':
            if len(stmnt.statements) > 0:
                hole_found = True  # Not necessarily a hole but fills will be found in recursion
                # Ennumerate sub statements
                skeleton_cpy = copy.deepcopy(skeleton)
                goto_stmt_cpy = skeleton_cpy.statements[goto_iter_count]

                # Fix sub statements
                stmt_depth.append(stmt_iter_count)
                stmnt_cpy = skeleton_cpy.statements[goto_iter_count]

                for i in stmt_depth:
                    stmnt_cpy = stmnt_cpy.statements[i]

                completed_progs = completed_progs + sub_statement_ennumerator_v0(
                    env, skeleton_cpy, goto_stmt_cpy, stmnt_cpy, goto_iter_count, stmt_depth)

                stmt_depth.pop(-1)

            break

        # Check each type of statement
        if type(stmnt) is Scan:
            # Check if object type is a hole
            if stmnt.obj_tp == None:
                hole_found = True

                # Loop through possible objects that can fill hole
                for obj_tp in env_def.object_types:
                    stmnt.obj_tp = obj_tp

                    skeleton_cpy = copy.deepcopy(skeleton)
                    goto_stmnt_cp = skeleton_cpy.statements[goto_iter_count]
                    top_level_stmnt_cp = skeleton_cpy.statements[goto_iter_count]
                    for i in stmt_depth:
                        top_level_stmnt_cp = top_level_stmnt_cp.statements[i]

                    completed_progs = completed_progs + sub_statement_ennumerator_v0(
                        env, skeleton_cpy, goto_stmnt_cp, top_level_stmnt_cp, goto_iter_count, stmt_depth)

                break

        elif type(stmnt) is Let:
            if stmnt.i == None:
                hole_found = True

                # Allow i from 0 to 10
                for i in range(10):
                    stmnt.i = i

                    skeleton_cpy = copy.deepcopy(skeleton)
                    goto_stmnt_cp = skeleton_cpy.statements[goto_iter_count]
                    top_level_stmnt_cp = skeleton_cpy.statements[goto_iter_count]
                    for i in stmt_depth:
                        top_level_stmnt_cp = top_level_stmnt_cp.statements[i]

                    completed_progs = completed_progs + sub_statement_ennumerator_v0(
                        env, skeleton_cpy, goto_stmnt_cp, top_level_stmnt_cp, goto_iter_count, stmt_depth)

                break
            elif stmnt.v_bar == None:
                hole_found = True

                # Get possible object sets from relevant scans
                pot_object_sets = get_object_set(goto_stmt, stmnt)

                for obj_set in pot_object_sets:
                    stmnt.v_bar = obj_set

                    skeleton_cpy = copy.deepcopy(skeleton)
                    goto_stmnt_cp = skeleton_cpy.statements[goto_iter_count]
                    top_level_stmnt_cp = skeleton_cpy.statements[goto_iter_count]
                    for i in stmt_depth:
                        top_level_stmnt_cp = top_level_stmnt_cp.statements[i]

                    completed_progs = completed_progs + sub_statement_ennumerator_v0(
                        env, skeleton_cpy, goto_stmnt_cp, top_level_stmnt_cp, goto_iter_count, stmt_depth)

                break

        elif type(stmnt) is Foreach_obj:
            if stmnt.obj_set == None:
                hole_found = True

                # Get possible object sets from relevant scans
                pot_object_sets = get_object_set(goto_stmt, stmnt)

                for obj_set in pot_object_sets:
                    stmnt.obj_set = obj_set

                    skeleton_cpy = copy.deepcopy(skeleton)
                    goto_stmnt_cp = skeleton_cpy.statements[goto_iter_count]
                    top_level_stmnt_cp = skeleton_cpy.statements[goto_iter_count]
                    for i in stmt_depth:
                        top_level_stmnt_cp = top_level_stmnt_cp.statements[i]

                    completed_progs = completed_progs + sub_statement_ennumerator_v0(
                        env, skeleton_cpy, goto_stmnt_cp, top_level_stmnt_cp, goto_iter_count, stmt_depth)

            if len(stmnt.statements) > 0:
                hole_found = True  # Not necessarily a hole but fills will be found in recursion
                # Ennumerate sub statements
                skeleton_cpy = copy.deepcopy(skeleton)

                goto_stmnt_cp = skeleton_cpy.statements[goto_iter_count]

                # Fix sub statements
                stmt_depth.append(stmt_iter_count)
                stmnt_cpy = skeleton_cpy.statements[goto_iter_count]

                for i in stmt_depth:
                    stmnt_cpy = stmnt_cpy.statements[i]

                completed_progs = completed_progs + sub_statement_ennumerator_v0(
                    env, skeleton_cpy, goto_stmnt_cp, stmnt_cpy, goto_iter_count, stmt_depth)

                stmt_depth.pop(-1)

        elif type(stmnt) is If:
            #Get potential fills for the bexp hole
            bexp_set = bexp_hole_find_fill(stmnt.bexp, goto_stmt, stmnt)

            if len(bexp_set) > 1: #Holes were present
                hole_found = True
                # Iterate over possible Expressions
                for bexp in bexp_set:
                    stmnt.bexp = bexp

                    skeleton_cpy = copy.deepcopy(skeleton)
                    goto_stmnt_cp = skeleton_cpy.statements[goto_iter_count]
                    top_level_stmnt_cp = skeleton_cpy.statements[goto_iter_count]
                    for i in stmt_depth:
                        top_level_stmnt_cp = top_level_stmnt_cp.statements[i]

                    completed_progs = completed_progs + sub_statement_ennumerator_v0(
                        env, skeleton_cpy, goto_stmnt_cp, top_level_stmnt_cp, goto_iter_count, stmt_depth)

            if len(stmnt.statements) > 0:
                hole_found = True #Not necessarily a hole but fills will be found in recursion
                # Ennumerate sub statements
                skeleton_cpy = copy.deepcopy(skeleton)

                goto_stmnt_cp = skeleton_cpy.statements[goto_iter_count]

                # Fix sub statements
                stmt_depth.append(stmt_iter_count)
                stmnt_cpy = skeleton_cpy.statements[goto_iter_count]

                for i in stmt_depth:
                    stmnt_cpy = stmnt_cpy.statements[i]

                completed_progs = completed_progs + sub_statement_ennumerator_v0(
                    env, skeleton_cpy, goto_stmnt_cp, stmnt_cpy, goto_iter_count, stmt_depth)

                stmt_depth.pop(-1)

        elif type(stmnt) is Act:
            if stmnt.obj == None:
                hole_found = True

                # Loop through possible objects that can fill hole
                pot_objects = get_objects(goto_stmt, stmnt)

                for obj in pot_objects:
                    stmnt.obj = obj

                    skeleton_cpy = copy.deepcopy(skeleton)
                    goto_stmnt_cp = skeleton_cpy.statements[goto_iter_count]
                    top_level_stmnt_cp = skeleton_cpy.statements[goto_iter_count]
                    for i in stmt_depth:
                        top_level_stmnt_cp = top_level_stmnt_cp.statements[i]

                    completed_progs = completed_progs + sub_statement_ennumerator_v0(
                        env, skeleton_cpy, goto_stmnt_cp, top_level_stmnt_cp, goto_iter_count, stmt_depth)

                break

            elif stmnt.action == None:
                hole_found = True

                # Get object types to iterate over based on stmnt.obj
                pot_types = get_types(goto_stmt, stmnt, stmnt.obj)

                for tp in pot_types:
                    for action in env_def.actions[tp]:
                        stmnt.action = action

                        skeleton_cpy = copy.deepcopy(skeleton)
                        goto_stmnt_cp = skeleton_cpy.statements[goto_iter_count]
                        top_level_stmnt_cp = skeleton_cpy.statements[goto_iter_count]
                        for i in stmt_depth:
                            top_level_stmnt_cp = top_level_stmnt_cp.statements[i]

                        completed_progs = completed_progs + sub_statement_ennumerator_v0(
                            env, skeleton_cpy, goto_stmnt_cp, top_level_stmnt_cp, goto_iter_count, stmt_depth)

                break

            elif stmnt.action == 'Place' and type(top_level_stmnt) is Goto and top_level_stmnt.loc != None:
                if len(stmnt.rel_set) == 0:
                    hole_found = True
                    #Iterate through objects and relations
                    for obj in env.locations[top_level_stmnt.loc.get_name()].objects:
                        for rel in env_def.relations:
                            print(type(obj))
                            assert 1 == 0
                            stmnt.rel_set = [(rel, obj)]

                            skeleton_cpy = copy.deepcopy(skeleton)
                            goto_stmnt_cp = skeleton_cpy.statements[goto_iter_count]
                            top_level_stmnt_cp = skeleton_cpy.statements[goto_iter_count]
                            for i in stmt_depth:
                                top_level_stmnt_cp = top_level_stmnt_cp.statements[i]

                            completed_progs = completed_progs + sub_statement_ennumerator_v0(
                                env, skeleton_cpy, goto_stmnt_cp, top_level_stmnt_cp, goto_iter_count, stmt_depth)

                else:
                    rel_count = 0
                    for rels in stmnt.rel_set:
                        if rels[0] == None:
                            hole_found = True

                            for rel in env_def.relations:
                                stmnt.rel_set[rel_count] = (rel, rels[1])

                                skeleton_cpy = copy.deepcopy(skeleton)
                                goto_stmnt_cp = skeleton_cpy.statements[goto_iter_count]
                                top_level_stmnt_cp = skeleton_cpy.statements[goto_iter_count]
                                for i in stmt_depth:
                                    top_level_stmnt_cp = top_level_stmnt_cp.statements[i]

                                completed_progs = completed_progs + sub_statement_ennumerator_v0(
                                    env, skeleton_cpy, goto_stmnt_cp, top_level_stmnt_cp, goto_iter_count, stmt_depth)

                        elif rels[1] == None:
                            hole_found = True

                            for obj in env.locations[top_level_stmnt.loc.get_name()].objects:
                                stmnt.rel_set[rel_count] = (rels[0], variable(obj))

                                skeleton_cpy = copy.deepcopy(skeleton)
                                goto_stmnt_cp = skeleton_cpy.statements[goto_iter_count]
                                top_level_stmnt_cp = skeleton_cpy.statements[goto_iter_count]
                                for i in stmt_depth:
                                    top_level_stmnt_cp = top_level_stmnt_cp.statements[i]

                                completed_progs = completed_progs + sub_statement_ennumerator_v0(
                                    env, skeleton_cpy, goto_stmnt_cp, top_level_stmnt_cp, goto_iter_count,
                                    stmt_depth)

                        rel_count = rel_count + 1

        stmt_iter_count = stmt_iter_count + 1

    # Append current skeleton if no hole found
    if not hole_found:
        completed_progs.append(skeleton)

    return completed_progs
