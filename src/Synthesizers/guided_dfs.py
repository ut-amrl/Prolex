from Synthesizers.find_hole import find_hole
from Synthesizers.ordered_hole_fills import ordered_hole_fills
from Synthesizers.fill_holes import fill_hole
from Synthesizers.check import *
from transformers import pipeline
from Synthesizers.infeasibility_check import *

import copy

def guided_dfs(sketch, demo, env, LM, num_checked=0, inf_caught=0, tp="GDFS", inf_check=False,
               out_result=None, inc_lock=None, prog_lock=None, lm_lock=None, done_event=None):
    if done_event != None and done_event.is_set():
        #Increment with num_checked
        out_result.inc_comp(num_checked)
        out_result.inc_inf(inf_caught)
        return None, num_checked, inf_caught, False

    #Get hole to fill
    hole_stmnt_pos, hole_idx = find_hole(sketch)

    #Check if sketch is complete
    if hole_stmnt_pos == None:
        num_checked = num_checked + 1

        #Check if correct
        if check(demo, sketch, copy.copy(env), printing=False): #Correct program
            #Correct prog found so wrap up threads
            if done_event != None and not done_event.is_set():
                done_event.set() #Signal other threads to complete
                # Increment with num_checked
                out_result.inc_comp(num_checked)
                out_result.inc_inf(inf_caught)

                #Put prog to output
                out_result.set_prog(sketch)

            return sketch, num_checked, inf_caught, False
        else: #Inocorrect Program
            #print(sketch.pretty_str(0))
            return None, num_checked, inf_caught, False

    # Get sorted order hole fills
    hole_fills_sorted = ordered_hole_fills(LM.LM, sketch, env, hole_stmnt_pos, hole_idx, demo, tp, lm_lock)

    if hole_fills_sorted == []:
        return None, num_checked, inf_caught, True

    #Loop through fills
    for fill in hole_fills_sorted:
        #Probably overkill to check here too
        if done_event != None and done_event.is_set():
            # Increment with num_checked
            out_result.inc_comp(num_checked)
            out_result.inc_inf(inf_caught)

            return None, num_checked, inf_caught, False

        new_sketch = fill_hole(deepcopy(sketch), hole_stmnt_pos, hole_idx, fill)

        #Check infeasibility
        #if inf_check and infeasible(new_sketch, demo, copy.copy(env)):
        #    inf_caught += 1
        #    continue
        if inf_check:
            #Check hole type
            stmnt = new_sketch
            for pos in hole_stmnt_pos:
                stmnt = stmnt.statements[pos]

            #Check that statement filled no longer has holes
            temp_hole_stmnt_pos, _ = find_hole(new_sketch)

            if hole_stmnt_pos != temp_hole_stmnt_pos:
                if infeasible(new_sketch, demo, copy.copy(env)):
                    inf_caught += 1
                    continue

        #Recursive Call
        prog, num_checked, inf_caught, no_sub_holes = guided_dfs(new_sketch, demo, env, LM, num_checked, inf_caught, tp, inf_check, out_result,
                                       inc_lock, prog_lock, lm_lock, done_event)

        if no_sub_holes:
            return None, num_checked, inf_caught, False

        if prog != None: #Found Program in subtree
            return prog, num_checked, inf_caught, False

    return None, num_checked, inf_caught, False
