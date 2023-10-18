from multiprocessing import Event
from multiprocessing import Process
from multiprocessing import Lock
from multiprocessing.managers import BaseManager
from multiprocessing import active_children

import time

from Synthesizers.guided_dfs import *
from Synthesizers.program_cleanup import *

import random

from exp_config import *

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
        self.LM = pipeline(model="bert-base-uncased", task="fill-mask", top_k=100)#, device=0)

def timeout(done_event, start_time):
    curr_time = time.time()

    while (curr_time - start_time) < timeout_in_min * 60:
        curr_time = time.time()

        if done_event.is_set():
            return

    #Timeout reached
    if not done_event.is_set():
       done_event.set() #Signal other threads to complete

def parallel_enumeration_no_sketch(sketch_list, demo, env, out_result, shared_LM, tp="GDFS", inf_check=False):
    #Make a new enumeration thread for each sketch
    inc_lock = Lock()
    prog_lock = Lock()
    lm_lock = Lock()

    done_event = Event()

    start_time = time.time()
    timeout_proc = Process(target=timeout, args=(done_event, start_time))

    random.shuffle(sketch_list)

    #sketch_list = sketch_list[0:40]

    #Call guided DFS for each sketch in new process
    processes = [Process(target=guided_dfs, args=(sketch_list[i], demo, env, shared_LM, 0, 0, tp, inf_check,
                        out_result, inc_lock, prog_lock, lm_lock, done_event)) for i in range(len(sketch_list))]

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

        while len(active_children()) > 8:
            if done_event.is_set():
                for p in started_processes:
                    p.kill()

                started_processes = []

                break

    for p in started_processes:
        if done_event.is_set():
            for p in started_processes:
                p.kill()

            started_processes = []
            break
        p.join()

    timeout_proc.join()

    #Cleanup program
    res_prog = out_result.get_prog()
    if res_prog != None:
        res_prog = prog_clean(res_prog)

    #Return results
    return res_prog, out_result.get_comp_checked(), out_result.get_inf_caught()
