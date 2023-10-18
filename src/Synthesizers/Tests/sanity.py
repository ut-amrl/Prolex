from Synthesizers.parallel_enumeration import *

import exp_config

import random
import time

from benchmark.Tasks.B1 import *
from benchmark.Tasks.B2 import *
from benchmark.Tasks.B3 import *
from benchmark.Tasks.B4 import *
from benchmark.Tasks.B5 import *
from benchmark.Tasks.B6 import *
from benchmark.Tasks.B8 import *
from benchmark.Tasks.B7 import *
from benchmark.Tasks.B9 import *
from benchmark.Tasks.B10 import *

from benchmark.Tasks.survey.S0 import *
from benchmark.Tasks.survey.S1 import *
from benchmark.Tasks.survey.S2 import *
from benchmark.Tasks.survey.S3 import *
from benchmark.Tasks.survey.S4 import *
from benchmark.Tasks.survey.S5 import *
from benchmark.Tasks.survey.S6 import *
from benchmark.Tasks.survey.S7 import *
from benchmark.Tasks.survey.S8 import *
from benchmark.Tasks.survey.S9 import *
from benchmark.Tasks.survey.S10 import *
from benchmark.Tasks.survey.S11 import *
from benchmark.Tasks.survey.S12 import *
from benchmark.Tasks.survey.S13 import *
from benchmark.Tasks.survey.S14 import *

from benchmark.Tasks.AdditionalBehavior.AB1 import *
from benchmark.Tasks.AdditionalBehavior.AB2 import *
from benchmark.Tasks.AdditionalBehavior.AB3 import *
from benchmark.Tasks.AdditionalBehavior.AB4 import *
from benchmark.Tasks.AdditionalBehavior.AB5 import *
from benchmark.Tasks.AdditionalBehavior.AB6 import *
from benchmark.Tasks.AdditionalBehavior.AB7 import *
from benchmark.Tasks.AdditionalBehavior.AB8 import *
from benchmark.Tasks.AdditionalBehavior.AB9 import *
from benchmark.Tasks.AdditionalBehavior.AB10 import *
from benchmark.Tasks.AdditionalBehavior.AB11 import *
from benchmark.Tasks.AdditionalBehavior.AB12 import *
from benchmark.Tasks.AdditionalBehavior.AB13 import *
from benchmark.Tasks.AdditionalBehavior.AB14 import *
from benchmark.Tasks.AdditionalBehavior.AB15 import *

from benchmark.Environments.E import *

if __name__ == "__main__":
    diff_list = ['e']
    llm_val = ['GDFS']
    inf_check = [True]

    for ALG_TYPE in llm_val:
        for INF_CHECK in inf_check:
            res_by_diff_list = []
            res_prog_list = []
            for diff in diff_list:
                exp_config.init(diff)

                prog_list = [B6_prog()]
                
                avg_vals_for_prog = []
                prog_idx = 0
                for prog in prog_list:
                    prog_idx += 1
                    avg_val_for_seed = []
                    for i in range(1): #####################TEMP############
                        random.seed(i)

                        num_traces = 1
                        env_and_demo_list = []
                        for xzy in range(num_traces):
                            env = E()

                            env = f(env, exp_config.extra_env_objs, exp_config.extra_env_rels)

                            #Calc num props
                            num_props = 0
                            num_objects = 0
                            for loc in env.locations:
                                for obj in env.locations[loc].objects:
                                    num_objects += 1
                                    num_props += len(env.locations[loc].objects[obj].props)

                            trace = prog.execute(deepcopy(env))
                            demo = trace[2]

                            env_and_demo_list.append((env, demo))

                        total_time_for_seed = 0
                        total_checked_for_seed = 0
                        total_inf_caught_for_seed = 0
                        num_correct_for_seed = 0
                        #Repeat same seed mutliple times to account for differences accross parallelization OS ordering
                        num_iter = 1
                        for j in range(num_iter):
                            start_time = time.time()
                            CustomManager.register('Enum_Result', Enum_Result)
                            CustomManager.register('LM_Def', LM_Def)

                            with CustomManager() as manager:
                                out_result = manager.Enum_Result()
                                shared_LM = manager.LM_Def()

                                sketches = []
                                ed_iter = 0
                                for (env, demo) in env_and_demo_list:
                                    if ed_iter == 0:
                                        sketches = gen_sketch_set(demo, env)

                                    else:
                                        temp_sketches = gen_sketch_set(demo, env)

                                        new_sk_list = []
                                        for alpha in temp_sketches:
                                            for beta in sketches:
                                                if alpha == beta and alpha not in new_sk_list:
                                                    new_sk_list.append(alpha)
                                                    break

                                        sketches = new_sk_list

                                    ed_iter += 1

                                #Try Parallel solving
                                ret_prog, num_checked, inf_caught = parallel_enumeration(sketches, demo, env, out_result, shared_LM, tp=ALG_TYPE, inf_check=INF_CHECK)

                                if ret_prog != None:
                                    res_prog_list.append((ret_prog, (diff, prog_idx, j)))
                               


                            end_time = time.time()

                            total_time_for_seed += (end_time - start_time)
                            if total_checked_for_seed + num_checked < 1e100:
                                total_checked_for_seed += num_checked
                            if total_inf_caught_for_seed + inf_caught < 1e100:
                                    total_inf_caught_for_seed += inf_caught

                            if ret_prog != None:
                                num_correct_for_seed += 1

                        avg_val_for_seed.append({"time": total_time_for_seed/float(num_iter), "num_checked": total_checked_for_seed/float(num_iter),
                                                 "inf_caught": total_inf_caught_for_seed/float(num_iter), "avg_num_correct": num_correct_for_seed/float(num_iter)})

                        print("Update:")
                        for entry in avg_val_for_seed:
                            print(entry)

                    #Append vals
                    avg_time_for_prog = 0
                    avg_checked_for_prog = 0
                    avg_inf_caught_for_prog = 0
                    avg_num_correct_for_prog = 0
                    for entry in avg_val_for_seed:
                        avg_time_for_prog += entry['time'] / len(avg_val_for_seed)
                        avg_checked_for_prog += entry['num_checked'] / len(avg_val_for_seed)
                        avg_inf_caught_for_prog += entry['inf_caught'] / len(avg_val_for_seed)
                        avg_num_correct_for_prog += entry['avg_num_correct'] / len(avg_val_for_seed)

                    avg_vals_for_prog.append({"time": avg_time_for_prog, "num_checked": avg_checked_for_prog,
                                             "inf_caught": avg_inf_caught_for_prog, "correct_percent": avg_num_correct_for_prog})

                    print("Prog Updated")
                    for entry in avg_vals_for_prog:
                        print(entry)

                res_by_diff_list.append(avg_vals_for_prog)

                
                print("New Difficulty")
                for row in res_by_diff_list:
                    print("ROW")
                    for entry in row:
                        print(entry)
