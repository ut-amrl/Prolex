from Synthesizers.get_hole_sentence import *
from Synthesizers.lm import *
import random

import exp_config

#TODO: Add priority value for Probability Prioritized Search

#TODO: Create and "all targets" which gives real potential fills for all holes then reduce return to only hole fills relevant for current hole

def ordered_hole_fills(LM, sketch, env, hole_stmnt_pos, hole_idx, demo, tp="", lm_lock=None):
    #Get statement
    goto_stmnt = None
    stmnt = sketch
    for pos in hole_stmnt_pos:
        if type(stmnt) is Goto:
            goto_stmnt = stmnt

        stmnt = stmnt.statements[pos]

    if type(stmnt) is Goto:
        #Default ordering is the only one that makes sense here
        locs = []

        for d_stmnt in demo.statements:
            if type(d_stmnt) is Goto_stmnt:
                locs.append(d_stmnt.loc)

        ret_locs = []
        for loc in locs:
            ret_locs.append(loc)

        random.shuffle(ret_locs)

        if tp == "GDFS":
            # Get context for LLM
            hole_pos, _, context_sentence = get_hole_context(sketch, sketch, hole_stmnt_pos)

            lm_locs = []
            for loc in ret_locs:
                #Fix with vocab
                temp_loc = loc.split('_')[0]
                if temp_loc == "Washroom":
                    temp_loc = "Bathroom"
                if temp_loc == "Livingroom":
                    temp_loc = "Parlor"

                lm_locs.append(temp_loc)

            # Get ordering from LLM
            if lm_lock != None:
                lm_lock.acquire()
            completions = most_likely_completion(lm_locs, context_sentence, LM, hole=hole_pos)
            if lm_lock != None:
                lm_lock.release()

            #Get location type counts from env
            bdr_ct = 0
            k_ct = 0
            lr_ct = 0
            bth_ct = 0
            for loc in env.locations:
                temp_loc = loc.split('_')[0]
                if temp_loc == "Bedroom":
                    bdr_ct = bdr_ct + 1
                if temp_loc == "Kitchen":
                    k_ct = k_ct + 1
                if temp_loc == "Livingroom":
                    lr_ct = lr_ct + 1
                if temp_loc == "Washroom":
                    bth_ct = bth_ct + 1


            ret_completions = []
            for loc in completions:
                temp_loc = loc[1]
                if temp_loc == "kitchen":
                    for i in range(k_ct):
                        add_loc = "Kitchen_" + str(i+1)
                        ret_completions.append(add_loc)

                if temp_loc == "parlor":
                    for i in range(lr_ct):
                        add_loc = "Livingroom_" + str(i+1)
                        ret_completions.append(add_loc)

                if temp_loc == "bathroom":
                    for i in range(bth_ct):
                        add_loc = "Washroom_" + str(i+1)
                        ret_completions.append(add_loc)

                if temp_loc == "bedroom":
                    for i in range(bdr_ct):
                        add_loc = "Bedroom_" + str(i+1)
                        ret_completions.append(add_loc)



            if ret_completions == []:
                for loc in ret_locs:
                    ret_completions.append(loc)

            return ret_completions

        return ret_locs

    if type(stmnt) is Scan:
        #Determine ordering
        if tp == "GDFS":
            #Possible objects
            potential_object_set = exp_config.env_def.object_types
            random.shuffle(potential_object_set)

            #Get context for LLM
            hole_pos, _, context_sentence = get_hole_context(sketch, sketch, hole_stmnt_pos)

            #Get ordering from LLM
            if lm_lock != None:
                lm_lock.acquire()
            completions = most_likely_completion(potential_object_set, context_sentence, LM, hole=hole_pos)
            if lm_lock != None:
                lm_lock.release()

            ret_completions = []
            for obj_tp in completions:
                ret_completions.append(obj_tp[1].capitalize())

            return ret_completions

        else:
            #Default ordering
            obj_types = exp_config.env_def.object_types
            random.shuffle(obj_types)
            return obj_types

    if type(stmnt) is Let:
        if hole_idx == 0:
            #Get object sets
            if tp == "GDFS":
                pot_object_sets = get_object_set(goto_stmnt, stmnt, True)

                if stmnt.obj_tp != None:
                    temp_pot_obj_sets = []
                    not_none_or_blank = 0
                    for obj_set in pot_object_sets:
                        if obj_set[1] == stmnt.obj_tp:
                            temp_pot_obj_sets.append(obj_set)
                        if obj_set[1] != None and obj_set[1] != "":
                            not_none_or_blank = not_none_or_blank + 1

                    if temp_pot_obj_sets != []:
                        ret_obj_set = []
                        for obj_set in temp_pot_obj_sets:
                            ret_obj_set.append(obj_set[0])

                        return ret_obj_set
                    elif not_none_or_blank > 0:
                        #All scans set but none fit
                        return []

                ret_obj_sets = []
                for pot_obj_set in pot_object_sets:
                    ret_obj_sets.append(pot_obj_set[0])
                return ret_obj_sets

            obj_set = get_object_set(goto_stmnt, stmnt)
            random.shuffle(obj_set)
            return obj_set

        if hole_idx == 1:
            #Return iterator numbers
            return [(i + stmnt.inst) for i in range(3)]

    if type(stmnt) is If:
        if hole_idx == 0:
            #Whole if is hole
            if stmnt.bexp == None:
                bexp_list = []

                #True is most likely
                bexp_list.append(Bexp('True', None, None))

                checkprop = Check_prop(None, None, None)
                checkrel = Check_rel(None, None, None, None, None)

                #Single/negs
                bexp_list.append(Bexp('single', deepcopy(checkprop)))
                bexp_list.append(Bexp('single', deepcopy(checkrel)))
                bexp_list.append(Bexp('neg', deepcopy(checkprop)))
                bexp_list.append(Bexp('neg', deepcopy(checkrel)))

                #Ands
                bexp_list.append(Bexp('and', deepcopy(checkprop), deepcopy(checkprop)))
                bexp_list.append(Bexp('and', deepcopy(checkprop), deepcopy(checkrel)))
                bexp_list.append(Bexp('and', deepcopy(checkrel), deepcopy(checkrel)))

                #Ors
                bexp_list.append(Bexp('or', deepcopy(checkprop), deepcopy(checkprop)))
                bexp_list.append(Bexp('or', deepcopy(checkprop), deepcopy(checkrel)))
                bexp_list.append(Bexp('or', deepcopy(checkrel), deepcopy(checkrel)))

                #False is unlikely
                bexp_list.append(Bexp('False', None, None))

                #Default ordering is valid here
                return bexp_list
            else: #Just need to determine from and/or/single/neg
                if stmnt.bexp.left == None:
                    return ['single', 'neg']
                else:
                    return ['and', 'or']
        if hole_idx == 1 or hole_idx == 2:
            if hole_idx == 1:
                check = stmnt.bexp.left
            elif hole_idx == 2:
                check = stmnt.bexp.right

            if check == None:
                return [Check_prop(None, None), Check_rel(None, None, None)]

            if type(check) is Check_prop:
                if check.obj == None:
                    pot_objects = get_objects_w_types(goto_stmnt, stmnt)
                    random.shuffle(pot_objects)

                    # If type is knonw check which potential object types match prop
                    if check.obj_tp != None:
                        temp_pot_obj = []
                        not_none_or_blank = 0
                        for pot_obj in pot_objects:
                            for pot_obj_tp in pot_obj[1]:
                                if check.obj_tp in pot_obj_tp:
                                    temp_pot_obj.append(pot_obj)
                                if pot_obj_tp != None and pot_obj_tp != "":
                                    not_none_or_blank = not_none_or_blank + 1

                        if temp_pot_obj != []:
                            # Don't need context here, can only be one of the above object sets
                            pot_objects = temp_pot_obj

                            ret_objs = []
                            for pot_obj in pot_objects:
                                ret_objs.append(pot_obj[0])

                            return ret_objs
                        elif not_none_or_blank == len(pot_objects):
                            # All obj_tps set but none valid
                            return []

                    # If prop is known, check which potential object types match prop
                    if check.obj_prop != None:
                        temp_pot_obj = []
                        not_none_or_blank = 0
                        for pot_obj in pot_objects:
                            for pot_obj_tp in pot_obj[1]:
                                if check.obj_prop in exp_config.env_def.properties[pot_obj_tp]:
                                    temp_pot_obj.append(pot_obj)

                                if pot_obj_tp != None and pot_obj_tp != "":
                                    not_none_or_blank = not_none_or_blank + 1

                        if temp_pot_obj != []:
                            pot_objects = temp_pot_obj

                            ret_objs = []
                            for pot_obj in pot_objects:
                                ret_objs.append(pot_obj[0])

                            if len(ret_objs) > 1 and tp == "GDFS":
                                # WITH CONTEXT from LLM
                                # Get context based on object types

                                potential_object_set = []
                                for obj_list in pot_objects:
                                    for obj in obj_list[1]:
                                        if obj not in potential_object_set:
                                            potential_object_set.append(obj)

                                # Get context for LLM
                                hole_pos, _, context_sentence = get_hole_context(sketch, sketch, hole_stmnt_pos)

                                # Get ordering from LLM
                                if lm_lock != None:
                                    lm_lock.acquire()

                                completions = most_likely_completion(potential_object_set, context_sentence, LM,
                                                                     hole=hole_pos)
                                if lm_lock != None:
                                    lm_lock.release()

                                # Capitalize
                                ret_completions = []
                                for obj_tp in completions:
                                    ret_completions.append(obj_tp[1].capitalize())

                                # Find where corresponding Iterators/Vars
                                iter_var_ret = []
                                for ret_obj in ret_completions:
                                    for pot_objs in pot_objects:
                                        for pot_obj in pot_objs[1]:
                                            if pot_obj == ret_obj:
                                                iter_var_ret.append(pot_objs[0])

                                return iter_var_ret
                            else:
                                return ret_objs

                        elif not_none_or_blank == len(pot_objects):
                            # All obj_tps set but none valid
                            return []


                    if tp == "GDFS":
                        #WITH CONTEXT from LLM
                        #Get context based on object types

                        potential_object_set = []
                        for obj_list in pot_objects:
                            for obj in obj_list[1]:
                                if obj not in potential_object_set:
                                    potential_object_set.append(obj)

                        # Get context for LLM
                        hole_pos, _, context_sentence = get_hole_context(sketch, sketch, hole_stmnt_pos)

                        # Get ordering from LLM
                        if lm_lock != None:
                            lm_lock.acquire()
                        completions = most_likely_completion(potential_object_set, context_sentence, LM, hole=hole_pos)
                        if lm_lock != None:
                            lm_lock.release()

                        #Capitalize
                        ret_completions = []
                        for obj_tp in completions:
                            ret_completions.append(obj_tp[1].capitalize())

                        #Find where corresponding Iterators/Vars
                        iter_var_ret = []
                        for ret_obj in ret_completions:
                            for pot_objs in pot_objects:
                                for pot_obj in pot_objs[1]:
                                    if pot_obj == ret_obj:
                                        iter_var_ret.append(pot_objs[0])

                        return iter_var_ret

                    else:
                        #Default Order
                        ret_pot_objs = []
                        for pot_obj in pot_objects:
                            ret_pot_objs.append(pot_obj[0])

                        return ret_pot_objs

                if check.obj_prop == None:
                    #If object type is known fill with potential properties
                    if check.obj != None:
                        #Default Order
                        types = get_types(goto_stmnt, stmnt, check.obj)
                        random.shuffle(types)
                        props_list = []
                        for otp in types:
                            for prop in exp_config.env_def.properties[otp]:
                                props_list.append(prop)

                        random.shuffle(props_list)

                        if tp == "GDFS":
                            # Get context for LLM
                            hole_pos, _, context_sentence = get_hole_context(sketch, sketch, hole_stmnt_pos)

                            # Get ordering from LLM
                            if lm_lock != None:
                                lm_lock.acquire()
                            completions = most_likely_completion(props_list, context_sentence, LM,
                                                                hole=hole_pos)

                            if lm_lock != None:
                                lm_lock.release()

                            ret_completions = []
                            for res in completions:
                                ret_completions.append(res[1].capitalize())

                            return ret_completions
                        else:
                            return props_list
                    else: #Return any possible property
                        prop_list = set()
                        for tp in exp_config.env_def.object_types:
                            for prop in exp_config.env_def.properties[tp]:
                                prop_list.add(prop)

                        if tp == "GDFS":
                            # Get context for LLM
                            hole_pos, _, context_sentence = get_hole_context(sketch, sketch, hole_stmnt_pos)

                            # Get ordering from LLM
                            if lm_lock != None:
                                lm_lock.acquire()
                            completions = most_likely_completion(prop_list, context_sentence, LM,
                                                                 hole=hole_pos)

                            if lm_lock != None:
                                lm_lock.release()

                            ret_completions = []
                            for res in completions:
                                ret_completions.append(res[1].capitalize())

                            return ret_completions
                        else:
                            random.shuffle(prop_list)
                            return prop_list

            if type(check) is Check_rel:
                if check.obj1 == None:
                    pot_objects = get_objects_w_types(goto_stmnt, stmnt)
                    random.shuffle(pot_objects)

                    # If type is knonw check which potential object types match prop
                    if check.obj1_tp != None:
                        temp_pot_obj = []
                        not_none_or_blank = 0
                        for pot_obj in pot_objects:
                            for pot_obj_tp in pot_obj[1]:
                                if check.obj1_tp in pot_obj_tp:
                                    temp_pot_obj.append(pot_obj)
                                if pot_obj_tp != None and pot_obj_tp != "":
                                    not_none_or_blank = not_none_or_blank + 1

                        if temp_pot_obj != []:
                            # Don't need context here, can only be one of the above object sets
                            pot_objects = temp_pot_obj

                            ret_objs = []
                            for pot_obj in pot_objects:
                                ret_objs.append(pot_obj[0])

                            return ret_objs
                        elif not_none_or_blank == len(pot_objects):
                            # All obj_tps set but none valid
                            return []

                    if tp == "GDFS":
                        #TODO: Order results for get_objecst
                        return get_objects(goto_stmnt, stmnt)
                    else:
                        #Default Order
                        objs = get_objects(goto_stmnt, stmnt)
                        random.shuffle(objs)
                        return objs

                if check.obj2 == None:
                    pot_objects = get_objects_w_types(goto_stmnt, stmnt)
                    random.shuffle(pot_objects)

                    # If type is knonw check which potential object types match prop
                    if check.obj2_tp != None:
                        temp_pot_obj = []
                        not_none_or_blank = 0
                        for pot_obj in pot_objects:
                            for pot_obj_tp in pot_obj[1]:
                                if check.obj2_tp in pot_obj_tp:
                                    temp_pot_obj.append(pot_obj)
                                if pot_obj_tp != None and pot_obj_tp != "":
                                    not_none_or_blank = not_none_or_blank + 1

                        if temp_pot_obj != []:
                            # Don't need context here, can only be one of the above object sets
                            pot_objects = temp_pot_obj

                            ret_objs = []
                            for pot_obj in pot_objects:
                                ret_objs.append(pot_obj[0])

                            return ret_objs
                        elif not_none_or_blank == len(pot_objects):
                            # All obj_tps set but none valid
                            return []

                    if tp == "GDFS":
                        # TODO: Order results for get_objecst
                        return get_objects(goto_stmnt, stmnt)
                    else:
                        # Default Order
                        objs = get_objects(goto_stmnt, stmnt)
                        random.shuffle(objs)
                        return objs

                if check.rel == None:
                    rel_list = []
                    for rel in exp_config.env_def.relations:
                        rel_list.append(rel)

                    if tp == "GDFS":
                        # Get context for LLM
                        hole_pos, _, context_sentence = get_hole_context(sketch, sketch, hole_stmnt_pos)

                        # Get ordering from LLM
                        if lm_lock != None:
                            lm_lock.acquire()

                        completions = most_likely_completion(rel_list, context_sentence, LM,
                                                             hole=hole_pos)

                        if lm_lock != None:
                            lm_lock.release()

                        ret_completions = []
                        for comp in completions:
                            ret_completions.append(comp[1].capitalize())

                        return ret_completions
                    else:
                        # Default Order
                        random.shuffle(rel_list)
                        return rel_list

    if type(stmnt) is Foreach_obj:
        #Default Order is fine #TODO: Think more about this
        return get_object_set(goto_stmnt, stmnt)

    if type(stmnt) is Act:
        if hole_idx == 0:
            # if stmnt.action != 'Place':
            #     if tp == "GDFS":
            #         #TODO: Order with context
            #         return get_objects(goto_stmnt, stmnt)
            #     else:
            #         #Default Ordering
            #         return get_objects(goto_stmnt, stmnt)
            # else:
            pot_objects = get_objects_w_types(goto_stmnt, stmnt)

            # If type is knonw check which potential object types match
            if stmnt.obj_tp != None:
                temp_pot_obj = []
                not_none_or_blank = 0
                for pot_obj in pot_objects:
                    for pot_obj_tp in pot_obj[1]:
                        if stmnt.obj_tp in pot_obj_tp:
                            temp_pot_obj.append(pot_obj)
                        if pot_obj_tp != None and pot_obj_tp != "":
                            not_none_or_blank = not_none_or_blank + 1

                if temp_pot_obj != []:
                    # Don't need context here, can only be one of the above object sets
                    pot_objects = temp_pot_obj

                    ret_objs = []
                    for pot_obj in pot_objects:
                        ret_objs.append(pot_obj[0])

                    return ret_objs
                else:#if not_none_or_blank == len(pot_objects):
                    # All obj_tps set but none valid
                    return []

            if tp == "GDFS":
                # TODO: Order with context
                ret_objs = []
                for pot_obj in pot_objects:
                    ret_objs.append(pot_obj[0])

                return ret_objs
                #assert 1 == 0
            else:
                #Check all possible object iterators
                ret_objs = []
                for pot_obj in pot_objects:
                    ret_objs.append(pot_obj[0])

                random.shuffle(ret_objs)
                return ret_objs

        if hole_idx == 1:
            if stmnt.rel_set == []:
                #Default Ordering
                rel_set = []
                for obj in env.locations[goto_stmnt.loc].objects:
                    for rel in exp_config.env_def.relations:
                        rel_set.append((rel, obj))

                #Default Ordering is fine here #TODO: THINK MORE
                return rel_set
            else:
                #Find objects to put here
                pot_objects = get_objects_w_types(goto_stmnt, stmnt)

                ret_objs = []
                for obj in pot_objects:
                    ret_objs.append(obj[0])

                return ret_objs
