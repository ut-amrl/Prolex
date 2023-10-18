from multiprocessing import Event
from multiprocessing import Process
from multiprocessing import Lock
from multiprocessing.managers import BaseManager

import time

from Synthesizers.worklist_sketch_completion_no_loop_bound import *
from Synthesizers.program_cleanup import *

from exp_config import *

import logging

class CustomManager(BaseManager):
    pass

class Enum_Result():
    def __init__(self):
        self.completions_checked = 0
        self.infeasible_caught = 0
        self.resultant_prog = None

    def inc_comp(self, amt):
        self.completions_checked += amt

    def get_comp_checked(self):
        return self.completions_checked

    def inc_inf(self, amt):
        self.infeasible_caught += amt

    def get_inf_caught(self):
        return self.infeasible_caught

    def set_prog(self, prog):
        self.resultant_prog = prog

    def get_prog(self):
        return self.resultant_prog

class LM_Def():
    def __init__(self):
        self.LM = pipeline(model="bert-base-uncased", task="fill-mask", top_k=100, device=0)

def timeout(done_event, start_time):
    curr_time = time.time()

    while (curr_time - start_time) < timeout_in_min * 60:
        curr_time = time.time()

        if done_event.is_set():
            return

    #Timeout reached
    if not done_event.is_set():
       done_event.set() #Signal other threads to complete

def parallel_enumeration_no_loop_bound(sketch_list, demo, env, out_result, shared_LM, tp="GDFS", inf_check=False):
    #Make a new enumeration thread for each sketch
    inc_lock = Lock()
    prog_lock = Lock()
    lm_lock = Lock()

    done_event = Event()

    start_time = time.time()
    timeout_proc = Process(target=timeout, args=(done_event, start_time))

    #Call guided DFS for each sketch in new process

    if tp == "GDFS":
        processes = [Process(target=complete_sketch_no_loop_bound, args=(sketch_list[i], demo, env, shared_LM, 0, 0, 
            tp, inf_check, out_result, inc_lock, prog_lock, lm_lock, done_event)) for i in range(len(sketch_list))]

    timeout_proc.start()

    #Wait for threads to finish
    started_processes = []
    for p in processes:
        if done_event.is_set():
            for p in started_processes:
                p.kill()

            started_processes = []
            break
        p.start()
        started_processes.append(p)

    for p in started_processes:
        if done_event.is_set():
            for p in started_processes:
                p.kill()

            started_processes = []
            break
        p.join()

    timeout_proc.join()

    #Cleanup program
    try:
        res_prog = out_result.get_prog()
    except:
        res_prog = None
    if res_prog != None:
        res_prog = prog_clean(res_prog)

    #Return results
    try:
        checked = out_result.get_comp_checked()
        inf = out_result.get_inf_caught()
    except:
        checked = 0
        inf = 0
    return res_prog, checked, inf
