import random
import sys
sys.path.append('../')
sys.path.append('../Env')
sys.path.append('../benchmark')
from dsl import *
from benchmark.Environments.f import *

def generate_sketch(top_level, hole_percentage):
    count_rand_holes = 0

    #Iterate through statements and flag where holes were generated to add when making demo from sketch
    #Based on hole_percentage
    for stmnt in top_level.statements:
        if type(stmnt) is Goto:
            #Recurse
            count_rand_holes += generate_sketch(stmnt, hole_percentage)

        if type(stmnt) is Scan:
            #No necessary holes here so randomly insert one
            sample = random.randint(0, 100)
            if sample < hole_percentage:
                stmnt.obj_tp_hole = True

                count_rand_holes += 1

        if type(stmnt) is If:
            #Insert Holes in Left
            check = stmnt.bexp.left
            if check != None:
                if type(check) is Check_prop:
                    #Random
                    sample = random.randint(0, 100)
                    if sample < hole_percentage:
                        check.obj_tp_hole = True
                        count_rand_holes += 1

                    sample = random.randint(0, 100)
                    if sample < hole_percentage:
                        check.obj_prop_hole = True
                        count_rand_holes += 1

                else:
                    #Random
                    sample = random.randint(0, 100)
                    if sample < hole_percentage:
                        check.obj1_tp_hole = True
                        count_rand_holes += 1

                    sample = random.randint(0, 100)
                    if sample < hole_percentage:
                        check.obj2_tp_hole = True
                        count_rand_holes += 1

                    sample = random.randint(0, 100)
                    if sample < hole_percentage:
                        check.rel_hole = True
                        count_rand_holes += 1

            # Insert Holes in Right
            check = stmnt.bexp.right
            if type(check) is Check_prop:
                #Random
                sample = random.randint(0, 100)
                if sample < hole_percentage:
                    check.obj_tp_hole = True
                    count_rand_holes += 1

                sample = random.randint(0, 100)
                if sample < hole_percentage:
                    check.obj_prop_hole = True
                    count_rand_holes += 1

            else:
                #Random
                sample = random.randint(0, 100)
                if sample < hole_percentage:
                    check.obj1_tp_hole = True
                    count_rand_holes += 1

                sample = random.randint(0, 100)
                if sample < hole_percentage:
                    check.obj2_tp_hole = True
                    count_rand_holes += 1

                sample = random.randint(0, 100)
                if sample < hole_percentage:
                    check.rel_hole = True
                    count_rand_holes += 1

            #Recurse on sub statements
            count_rand_holes += generate_sketch(stmnt, hole_percentage)

        if type(stmnt) is Foreach_obj:
            #Recurse on substatements
            count_rand_holes += generate_sketch(stmnt, hole_percentage)

    return count_rand_holes

def get_demo_w_holes(prog, env, difficulty, env_difficulty):
    rand_holes_made = 0
    while rand_holes_made == 0:
        sketch = deepcopy(prog)
        rand_holes_made = generate_sketch(sketch, difficulty)

    #Update env with env difficulty
    if env_difficulty == "MED":
        env = f(env, 100, 100)

    #Get Demo with holes from "sketch"
    trace = sketch.execute(env)
    demo = trace[2]

    #Update demo with holes
    demo.apply_holes()

    return demo, env

#Try to get list of tasks
# import os
# task_dir = os.listdir('../benchmark/Tasks')

# task_dir.remove('__init__.py')
# task_dir.remove('__pycache__')
# task_dir.remove('.DS_Store')

# task_names = []
# for file_name in task_dir:
#     task = file_name.rstrip('.py')
#     task_names.append(task)

# from importlib import import_module

# for task in task_names:
#     task_path = import_module(f'benchmark.Tasks.{task}')

#     task_func_name = task
#     if len(task_func_name.split('_')) == 1:
#         task_func_name = task_func_name.split('_')[0]

#         task_func = task_path.__getattribute__(f'{task_func_name}_prog')

#         curr_prog = task_func()

#         print(task)
#         print(curr_prog.pretty_str(0))
#         print(get_demo_w_holes(curr_prog,E(),EASY,"MED")[0].pretty_str(0))
