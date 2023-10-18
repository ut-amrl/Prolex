from benchmark.Environments.E import *
#from Env import env_def
from copy import deepcopy
import exp_config

import numpy as np

import sys

def encode_env(env, final=False):
    if final:
        mod_name = "_f"
        env_name = "final_env"
    else:
        mod_name = ""
        env_name = "init_env"

    base_object_dict = {}
    for obj_tp in exp_config.env_def.object_types:
        base_object_dict[obj_tp] = []

    loc_list = []
    for loc in env.locations:
        cur_loc = env.locations[loc]

        #Get objects
        cur_loc_objs_list = deepcopy(base_object_dict)
        for obj in cur_loc.objects:
            #Make object properties into a list of true/false
            cur_obj = cur_loc.objects[obj]

            obj_init_str = f"(define {obj}{mod_name} (list"
            for prop in cur_obj.props:
                if cur_obj.props[prop]:
                    obj_init_str += " #t"
                else:
                    obj_init_str += " #f"

            obj_init_str += "))"

            print(obj_init_str)

            if cur_obj.tp not in cur_loc_objs_list:
                cur_loc_objs_list[cur_obj.tp] = [obj]
            else:
                cur_loc_objs_list[cur_obj.tp].append(obj)
    
        # #Get relation true/false
        rel_list = []
        for rel in cur_loc.relations:
            obj1_tp = cur_loc.relations[rel].o1.tp
            obj1_name = cur_loc.relations[rel].o1.name
            obj1_tp_idx = exp_config.env_def.object_types.index(obj1_tp)
            obj1_inst_idx = cur_loc_objs_list[obj1_tp].index(obj1_name)

            obj2_tp = cur_loc.relations[rel].o2.tp
            obj2_name = cur_loc.relations[rel].o2.name
            obj2_tp_idx = exp_config.env_def.object_types.index(obj2_tp)
            obj2_inst_idx = cur_loc_objs_list[obj2_tp].index(obj2_name)

            rel_idx = exp_config.env_def.relations.index(cur_loc.relations[rel].tp)

            rel_list.append((obj1_tp_idx, obj1_inst_idx, obj2_tp_idx, obj2_inst_idx, rel_idx))

        rel_str = " (list"
        for rel in rel_list:
            rel_str += " (list " + str(rel[0]) + " " \
                       + str(rel[1]) + " " \
                       + str(rel[2]) + " " \
                       + str(rel[3]) + " " \
                       + str(rel[4]) + ")"
        
        #Setup location
        loc_init_str = f"(define {loc}{mod_name} (list (list"
        for obj in cur_loc_objs_list:
            loc_init_str += " (list"
            for obj_inst in cur_loc_objs_list[obj]:
                loc_init_str += f" {obj_inst}{mod_name}"

            loc_init_str += ")"

        loc_init_str += ") " + rel_str + ")))"

        print(loc_init_str)

        loc_list.append(loc)

    #Set up env
    init_env_str = f"(define {env_name} (list (list"
    for loc in loc_list:
        init_env_str += f" {loc}{mod_name}"


    init_env_str += ")"

    #Add string for robot objects
    rob_obj_str = "(list"
    for obj in base_object_dict:
        rob_obj_str += " (list)"

    init_env_str += rob_obj_str
    init_env_str += f") {loc_list.index(env.robot_loc)}))"

    print(init_env_str)

exp_config.init('e')

env = E()

og_stdout = sys.stdout

f = open('Test.rkt', 'w+')
sys.stdout = f

#File init
print("#lang rosette")

print("(require rosette/lib/angelic rosette/lib/destruct)")

print("(current-bitwidth #f)\n")

#Initial Env
encode_env(env)

#Get final env from execution
from benchmark.Tasks.survey.S14 import *

prog = S14()

final_env = prog.execute(env)[0][-1]

encode_env(final_env, final=True)

f.close()


