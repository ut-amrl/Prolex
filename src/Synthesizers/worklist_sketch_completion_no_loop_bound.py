from Synthesizers.find_hole import *
from Synthesizers.ordered_hole_fills_w_prob import ordered_hole_fills_w_prob
from Synthesizers.fill_holes import fill_hole
from Synthesizers.check import *
from transformers import pipeline
from Synthesizers.infeasibility_check_no_loop_bound import *

from queue import PriorityQueue

import copy

def complete_sketch_no_loop_bound(sketch, demo, env, LM, num_checked=0, inf_caught=0, tp="GDFS", inf_check=False,
               out_result=None, inc_lock=None, prog_lock=None, lm_lock=None, done_event=None):

    W = PriorityQueue()

    temp_hole_stmnt_pos, temp_hole_idx = find_hole(sketch)
    #temp_hole_stmnt_pos, temp_hole_idx = find_hole_best_hole(sketch, LM, env, demo, tp, lm_lock)
    #print("MAIN FUNC 1:", temp_hole_stmnt_pos)
    W.put((0, (sketch, (temp_hole_stmnt_pos, temp_hole_idx))))

    while not W.empty():
        (cur_prio, (cur_sketch, (hole_stmnt_pos, hole_idx))) = W.get()
        #print("MAIN FUNC 2:", hole_stmnt_pos)
        cur_prob = 1 - cur_prio

        #print(cur_sketch.pretty_str(0, debug=True))

        if done_event != None and done_event.is_set():
            #Increment with num_checked
            try:
                out_result.inc_comp(num_checked)
                out_result.inc_inf(inf_caught)
                return None, num_checked, inf_caught, False
            except:
                return None, num_checked, inf_caught, False

        # Get sorted order hole fills
        hole_fills_sorted, filled_by_LLM = ordered_hole_fills_w_prob(LM.LM, cur_sketch, env, hole_stmnt_pos, hole_idx, demo, tp, lm_lock)

        #print(hole_fills_sorted)

        if hole_fills_sorted == []:
            continue

        #Loop through fills and add to queue
        for prob, fill in hole_fills_sorted:
            #Probably overkill to check here too
            if done_event != None and done_event.is_set():
                # Increment with num_checked
                try:
                    out_result.inc_comp(num_checked)
                    out_result.inc_inf(inf_caught)

                    return None, num_checked, inf_caught, False
                except:    
                    return None, num_checked, inf_caught, False

            new_sketch = fill_hole(deepcopy(cur_sketch), hole_stmnt_pos, hole_idx, fill)

            #Check infeasibility
            if inf_check:
                #Check hole type
                stmnt = new_sketch
                for pos in hole_stmnt_pos:
                    stmnt = stmnt.statements[pos]

                #Check that statement filled no longer has holes
                #temp_hole_stmnt_pos, _ = find_hole(new_sketch)

                #if hole_stmnt_pos != temp_hole_stmnt_pos:
                if infeasible_no_loop_bound(new_sketch, demo, copy.copy(env)):
                    inf_caught += 1
                    continue

            #Check if sketch is complete -- Don't need to add to queue if complete and incorrect
            #Get hole to fill
            temp_hole_stmnt_pos, temp_hole_idx = find_hole(new_sketch)

            #temp_hole_stmnt_pos, temp_hole_idx = find_hole_best_hole(new_sketch, LM, env, demo, tp, lm_lock)

            #print("MAIN FUNC 3:", temp_hole_stmnt_pos)

            if temp_hole_stmnt_pos == None:
                num_checked = num_checked + 1

                #Check if correct
                if check(demo, new_sketch, copy.copy(env), printing=False): #Correct program
                    #Correct prog found so wrap up threads
                    if done_event != None and not done_event.is_set():
                        done_event.set() #Signal other threads to complete
                        # Increment with num_checked
                        out_result.inc_comp(num_checked)
                        out_result.inc_inf(inf_caught)

                        #Put prog to output
                        out_result.set_prog(new_sketch)

                    return new_sketch, num_checked, inf_caught, False
                else:
                    continue

            if filled_by_LLM:
                #Add to queue
                #print(f'New Priority: {1 - prob*cur_prob}, Current Prob: {cur_prob}, Pred Prob: {prob}')
                W.put((1 - prob, (new_sketch, (temp_hole_stmnt_pos, temp_hole_idx))))
            else: #Do Depth first here
                new_sketch, temp_num_checked, temp_inf_caught, _ = complete_sketch_no_loop_bound(new_sketch, demo, env, LM, num_checked, inf_caught, tp, inf_check, out_result, inc_lock, prog_lock, lm_lock, done_event)
                num_checked += temp_num_checked
                inf_caught += temp_inf_caught

                if new_sketch != None:
                    return new_sketch, num_checked, inf_caught, False
                

    return None, num_checked, inf_caught, False
