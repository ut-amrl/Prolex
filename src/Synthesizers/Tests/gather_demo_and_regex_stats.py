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

def calc_len(stmnts):
    num = 0
    for stmnt in stmnts:
        if type(stmnt) is Goto_stmnt:
            num += calc_len(stmnt.statements)
        num += 1

    return num

if __name__ == "__main__":
    diff_list = ['e','m','h']
    llm_val = ['GDFS']
    inf_check = [True]

    for ALG_TYPE in llm_val:
        for INF_CHECK in inf_check:
            res_by_diff_list = []
            res_prog_list = []
            for diff in diff_list:
                exp_config.init(diff)

                prog_list = [B1_prog(), B2_prog(), B3_prog(), B4_prog(), B5_prog(), B6_prog(), B7_prog(), B8_prog(), B9_prog(), B10_prog(), S0(), S1(), S2(), S3(), S4(), S5(), S6(), S7(), S8(), S9(), S10(), S11(), S12(), S13(), S14(), AB1(), AB2(), AB3(), AB4(), AB5(), AB6(), AB7(), AB8(), AB9(), AB10(), AB11(), AB12(), AB13(), AB14(), AB15()]
                
                avg_vals_for_prog = []
                prog_idx = 0
                for prog in prog_list:
                    prog_idx += 1
                    avg_val_for_seed = []
                    for i in range(1): #####################TEMP############
                        random.seed(i)

                        num_traces = 1
                        env_and_demo_list = []
                        demo_len = 0
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

                            demo_len = calc_len(demo.statements)

                            env_and_demo_list.append((env, demo))

                        #Repeat same seed mutliple times to account for differences accross parallelization OS ordering
                        num_iter = 1
                        for j in range(num_iter):
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

                        print("Sketch: ", len(sketches), " Demo: ", demo_len)

                print("New Difficulty")
