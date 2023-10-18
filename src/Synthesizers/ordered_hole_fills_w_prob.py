from Synthesizers.get_hole_sentence import *
from Synthesizers.lm_w_prob import *
import random

import exp_config

#TODO: Add priority value for Probability Prioritized Search

#TODO: Create and "all targets" which gives real potential fills for all holes then reduce return to only hole fills relevant for current hole

def ordered_hole_fills_w_prob(LM, sketch, env, hole_stmnt_pos, hole_idx, demo, tp="", lm_lock=None):
    
    #######################################
    # LM LOCK NOT NEEDED WITH OPEN AI API #
    #######################################

    #lm_lock = None

    filled_by_LLM = True

    #Get statement
    goto_stmnt = None
    stmnt = sketch

    #print("ORDERING FUNC:", hole_stmnt_pos)

    for pos in hole_stmnt_pos:
        if type(stmnt) is Goto:
            goto_stmnt = stmnt

        stmnt = stmnt.statements[pos]

    if type(stmnt) is Goto:
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

            #print("CHECKED FOR GOTO")

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
                        ret_completions.append((loc[0], add_loc))

                if temp_loc == "parlor":
                    for i in range(lr_ct):
                        add_loc = "Livingroom_" + str(i+1)
                        ret_completions.append((loc[0], add_loc))

                if temp_loc == "bathroom":
                    for i in range(bth_ct):
                        add_loc = "Washroom_" + str(i+1)
                        ret_completions.append((loc[0], add_loc))

                if temp_loc == "bedroom":
                    for i in range(bdr_ct):
                        add_loc = "Bedroom_" + str(i+1)
                        ret_completions.append((loc[0], add_loc))



            default_prob = 1/len(ret_locs)

            if ret_completions == []:
                filled_by_LLM = False
                for loc in ret_locs:
                    ret_completions.append((default_prob, loc))

            return ret_completions, filled_by_LLM
        else:
            #Should only be used with LLM version
            assert 1 == 0

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
            
            #Get trace from demo
            #trace = '['
            #demo_str = demo.pretty_str(0)
            #first = True
            #for line in demo_str.splitlines()[1::]:
            #    line = line.strip(' \t:')
            #    if first:
            #        trace += line
            #        first = False
            #    else:
            #        trace += ', ' + line

            #trace += ']'

            #completions = most_likely_completion_scan(potential_object_set, context_sentence, trace, LM, hole=hole_pos)
            completions = most_likely_completion(potential_object_set, context_sentence, LM, hole=hole_pos)
            #print("CHECKED FOR SCAN")
            if lm_lock != None:
                lm_lock.release()

            ret_completions = []
            for obj_tp in completions:
                ret_completions.append((obj_tp[0], obj_tp[1].capitalize()))

            #TEMP
            #return [(1.0, 'Table')], False

            return ret_completions, filled_by_LLM

        else:
            #Should only be used with LLM version
            assert 1 == 0

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
                        default_prob = 1/len(temp_pot_obj_sets)
                        ret_obj_set = []
                        for obj_set in temp_pot_obj_sets:
                            ret_obj_set.append((default_prob, obj_set[0]))

                        return ret_obj_set, False
                    elif not_none_or_blank > 0:
                        #All scans set but none fit
                        return [], False

                ret_obj_sets = []
                default_prob = 1 /len(pot_object_sets)
                for pot_obj_set in pot_object_sets:
                    ret_obj_sets.append((default_prob, pot_obj_set[0]))
                return ret_obj_sets, False

            else:
                #Should only be used with LLM version
                assert 1 == 0

        if hole_idx == 1:
            #Return iterator numbers
            ret_list = []
            for i in range(3):
                ret_list.append((1/3, i+stmnt.inst))
            return ret_list, False

    if type(stmnt) is If:
        if hole_idx == 0:
            #Whole if is hole
            if stmnt.bexp == None:
                bexp_list = []

                #True is most likely
                bexp_list.append((0.75, Bexp('True', None, None)))

                checkprop = Check_prop(None, None, None)
                checkrel = Check_rel(None, None, None, None, None)

                #Single/negs
                bexp_list.append((0.03, Bexp('single', deepcopy(checkprop))))
                bexp_list.append((0.03, Bexp('single', deepcopy(checkrel))))
                bexp_list.append((0.03, Bexp('neg', deepcopy(checkprop))))
                bexp_list.append((0.03, Bexp('neg', deepcopy(checkrel))))

                #Ands
                bexp_list.append((0.02, Bexp('and', deepcopy(checkprop), deepcopy(checkprop))))
                bexp_list.append((0.02, Bexp('and', deepcopy(checkprop), deepcopy(checkrel))))
                bexp_list.append((0.02, Bexp('and', deepcopy(checkrel), deepcopy(checkrel))))

                #Ors
                bexp_list.append((0.015, Bexp('or', deepcopy(checkprop), deepcopy(checkprop))))
                bexp_list.append((0.015, Bexp('or', deepcopy(checkprop), deepcopy(checkrel))))
                bexp_list.append((0.015, Bexp('or', deepcopy(checkrel), deepcopy(checkrel))))

                #False is unlikely
                bexp_list.append((0.0075, Bexp('False', None, None)))

                return bexp_list, False
            else: #Just need to determine from and/or/single/neg
                if stmnt.bexp.left == None:
                    return [(0.5, 'single'), (0.5, 'neg')], False
                else:
                    return [(0.5, 'and'), (0.5, 'or')], False
        if hole_idx == 1 or hole_idx == 2:
            if hole_idx == 1:
                check = stmnt.bexp.left
            elif hole_idx == 2:
                check = stmnt.bexp.right

            if check == None:
                return [(0.5, Check_prop(None, None)), (0.5, Check_rel(None, None, None))], False

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
                            default_prob = 1/len(pot_objects)
                            for pot_obj in pot_objects:
                                ret_objs.append((default_prob, pot_obj[0]))

                            return ret_objs, False
                        elif not_none_or_blank == len(pot_objects):
                            # All obj_tps set but none valid
                            return [], False

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
                            default_prob = 1/len(pot_objects)
                            for pot_obj in pot_objects:
                                ret_objs.append((default_prob, pot_obj[0]))

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


                                #print("CHECKED FOR IF 1")

                                # Capitalize
                                ret_completions = []
                                for obj_tp in completions:
                                    ret_completions.append((obj_tp[0], obj_tp[1].capitalize()))

                                # Find where corresponding Iterators/Vars
                                iter_var_ret = []
                                for ret_obj in ret_completions:
                                    for pot_objs in pot_objects:
                                        for pot_obj in pot_objs[1]:
                                            if pot_obj == ret_obj[1]:
                                                iter_var_ret.append((ret_obj[0], pot_objs[0]))

                                return iter_var_ret, filled_by_LLM
                            else:
                                return ret_objs, False

                        elif not_none_or_blank == len(pot_objects):
                            # All obj_tps set but none valid
                            return [], False


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

                        #print("CHECKED FOR IF 2")
                        
                        #Capitalize
                        ret_completions = []
                        for obj_tp in completions:
                            ret_completions.append((obj_tp[0], obj_tp[1].capitalize()))

                        #Find where corresponding Iterators/Vars
                        iter_var_ret = []
                        for ret_obj in ret_completions:
                            for pot_objs in pot_objects:
                                for pot_obj in pot_objs[1]:
                                    if pot_obj == ret_obj[1]:
                                        iter_var_ret.append((ret_obj[0], pot_objs[0]))

                        return iter_var_ret, filled_by_LLM

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

                            #print("CHECKED FOR IF 3")
    
                            ret_completions = []
                            for res in completions:
                                ret_completions.append((res[0], res[1].capitalize()))

                            return ret_completions, filled_by_LLM
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

                            #print("CHECKED FOR IF 4")
                            
                            ret_completions = []
                            for res in completions:
                                ret_completions.append((res[0], res[1].capitalize()))

                            return ret_completions, filled_by_LLM

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
                            default_prob = 1/len(pot_objects)
                            for pot_obj in pot_objects:
                                ret_objs.append((default_prob, pot_obj[0]))

                            return ret_objs, False
                        elif not_none_or_blank == len(pot_objects):
                            # All obj_tps set but none valid
                            return [], False

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

                        #print("CHECKED FOR IF 5")
                        
                        #Capitalize
                        ret_completions = []
                        for obj_tp in completions:
                            ret_completions.append((obj_tp[0], obj_tp[1].capitalize()))

                        #Find where corresponding Iterators/Vars
                        iter_var_ret = []
                        for ret_obj in ret_completions:
                            for pot_objs in pot_objects:
                                for pot_obj in pot_objs[1]:
                                    if pot_obj == ret_obj[1]:
                                        iter_var_ret.append((ret_obj[0], pot_objs[0]))

                        return iter_var_ret, filled_by_LLM

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
                            default_prob = 1 / len(pot_objects)
                            for pot_obj in pot_objects:
                                ret_objs.append((default_prob, pot_obj[0]))

                            return ret_objs, False
                        elif not_none_or_blank == len(pot_objects):
                            # All obj_tps set but none valid
                            return [], False

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
                        
                        #print("CHECKED FOR IF 6")

                        #Capitalize
                        ret_completions = []
                        for obj_tp in completions:
                            ret_completions.append((obj_tp[0], obj_tp[1].capitalize()))

                        #Find where corresponding Iterators/Vars
                        iter_var_ret = []
                        for ret_obj in ret_completions:
                            for pot_objs in pot_objects:
                                for pot_obj in pot_objs[1]:
                                    if pot_obj == ret_obj[1]:
                                        iter_var_ret.append((ret_obj[0], pot_objs[0]))

                        return iter_var_ret, filled_by_LLM

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
                        
                        #print("CHECKED FOR IF 7")

                        ret_completions = []
                        for comp in completions:
                            ret_completions.append((comp[0], comp[1].capitalize()))

                        return ret_completions, filled_by_LLM

    if type(stmnt) is Foreach_obj:
        #Default Order is fine #TODO: Think more about this
        ret_obj_set = []
        valid_obj_tps = get_valid_obj_tps(stmnt)
        obj_set = get_object_set(goto_stmnt, stmnt, return_types=True)
        default_prob = 1/len(obj_set)
        for obj, tp in obj_set:
            if tp in valid_obj_tps:
                ret_obj_set.append((default_prob, obj))

        return ret_obj_set, False

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
                    default_prob = 1 / len(pot_objects)
                    for pot_obj in pot_objects:
                        ret_objs.append((default_prob, pot_obj[0]))

                    return ret_objs, False
                else:#if not_none_or_blank == len(pot_objects):
                    # All obj_tps set but none valid
                    return [], False

            if tp == "GDFS":
                # TODO: Order with context
                assert 1 == 0
                ret_objs = []
                for pot_obj in pot_objects:
                    ret_objs.append(pot_obj[0])

                return ret_objs
                #assert 1 == 0

        if hole_idx == 1:
            if stmnt.rel_set == []:
                #Default Ordering
                rel_set = []
                default_prob = 1/(len(env.locations[goto_stmnt.loc].objects)*len(exp_config.env_def.relations))
                for obj in env.locations[goto_stmnt.loc].objects:
                    for rel in exp_config.env_def.relations:
                        rel_set.append((default_prob, (rel, obj)))

                #Default Ordering is fine here #TODO: THINK MORE
                return rel_set, False
            else:
                #Find objects to put here
                pot_objects = get_objects_w_types(goto_stmnt, stmnt)

                ret_objs = []
                default_prob = 1/len(pot_objects)
                for obj in pot_objects:
                    ret_objs.append((default_prob, obj[0]))

                return ret_objs, False
