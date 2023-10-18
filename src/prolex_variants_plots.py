from data_parsers import Prolex_data_parser
from data_parsers import Prolex_NoLLM_data_parser
from data_parsers import Prolex_NoLoopBound_data_parser
from data_parsers import Prolex_NoPrune_data_parser
from data_parsers import Prolex_NoSketch_data_parser
from data_parsers import Prolex_SketchOnly_data_parser

import matplotlib.pyplot as plt

if __name__ == '__main__':

    ##########
    # PROLEX #
    ##########

    res = Prolex_data_parser.parse()

    # Get Num Completions accross all envs
    num_complete = 0
    total_num = 0
    for env in res:
        for task in res[env]:
            if res[env][task]['correct_percent'] == 1.0:
                num_complete += 1

            total_num += 1

    percent_complete_prolex = float(num_complete)/total_num*100
    print(f'Percent Complete PROLEX: {percent_complete_prolex}%')

    # Get Completion times for each env
    time_complete_percent = []
    for env in res:
        for task in res[env]:
            if res[env][task]['correct_percent'] == 1.0:
                time_complete_percent.append(res[env][task]['time'])

    # Set up plot arrays
    x_prolex = []
    y_prolex = []
    for task in time_complete_percent:
        x_prolex.append(task)

    x_prolex.sort()
    num_complete = 0
    for val in x_prolex:
        num_complete += 1
        y_prolex.append(float(num_complete)/120*100)
    
    ##################
    # PROLEX NoPrune #
    ##################

    res = Prolex_NoPrune_data_parser.parse()

    # Get Num Completions accross all envs
    num_complete = 0
    total_num = 0
    for env in res:
        for task in res[env]:
            if res[env][task]['correct_percent'] == 1.0:
                num_complete += 1

            total_num += 1

    percent_complete_no_prune = float(num_complete)/total_num*100
    print(f'Percent Complete NoPrune: {percent_complete_no_prune}%, Difference from Prolex: {abs(percent_complete_prolex-percent_complete_no_prune)}%')

    # Get Completion times for each env
    time_complete_percent = []
    for env in res:
        for task in res[env]:
            if res[env][task]['correct_percent'] == 1.0:
                time_complete_percent.append(res[env][task]['time'])

    # Set up plot arrays
    x_no_prune = []
    y_no_prune = []
    for task in time_complete_percent:
        x_no_prune.append(task)

    x_no_prune.sort()
    num_complete = 0
    for val in x_no_prune:
        num_complete += 1
        y_no_prune.append(float(num_complete)/120*100)
    
    ################
    # PROLEX NoLLM #
    ################

    res = Prolex_NoLLM_data_parser.parse()

    # Get Num Completions accross all envs
    num_complete = 0
    total_num = 0
    for env in res:
        for task in res[env]:
            if res[env][task]['correct_percent'] == 1.0:
                num_complete += 1

            total_num += 1

    percent_complete_no_llm = float(num_complete)/total_num*100
    print(f'Percent Complete NoLLM: {percent_complete_no_llm}%, Difference from Prolex: {abs(percent_complete_prolex-percent_complete_no_llm)}%')

    # Get Completion times for each env
    time_complete_percent = []
    for env in res:
        for task in res[env]:
            if res[env][task]['correct_percent'] == 1.0:
                time_complete_percent.append(res[env][task]['time'])

    # Set up plot arrays
    x_no_llm = []
    y_no_llm = []
    for task in time_complete_percent:
        x_no_llm.append(task)

    x_no_llm.sort()
    num_complete = 0
    for val in x_no_llm:
        num_complete += 1
        y_no_llm.append(float(num_complete)/120*100)

    #####################
    # PROLEX SketchOnly #
    #####################

    res = Prolex_SketchOnly_data_parser.parse()

    # Get Num Completions accross all envs
    num_complete = 0
    total_num = 0
    for env in res:
        for task in res[env]:
            if res[env][task]['correct_percent'] == 1.0:
                num_complete += 1

            total_num += 1

    percent_complete_sketch_only = float(num_complete)/total_num*100
    print(f'Percent Complete SketchOnly: {percent_complete_sketch_only}%, Difference from Prolex: {abs(percent_complete_prolex-percent_complete_sketch_only)}%')

    # Get Completion times for each env
    time_complete_percent = []
    for env in res:
        for task in res[env]:
            if res[env][task]['correct_percent'] == 1.0:
                time_complete_percent.append(res[env][task]['time'])

    # Set up plot arrays
    x_sketch_only = []
    y_sketch_only = []
    for task in time_complete_percent:
        x_sketch_only.append(task)

    x_sketch_only.sort()
    num_complete = 0
    for val in x_sketch_only:
        num_complete += 1
        y_sketch_only.append(float(num_complete)/120*100)

    ######################
    # PROLEX NoLoopBound #
    ######################

    res = Prolex_NoLoopBound_data_parser.parse()

    # Get Num Completions accross all envs
    num_complete = 0
    total_num = 0
    for env in res:
        for task in res[env]:
            if res[env][task]['correct_percent'] == 1.0:
                num_complete += 1

            total_num += 1

    percent_complete_no_loop_bound = float(num_complete)/total_num*100
    print(f'Percent Complete NoLoopBound: {percent_complete_no_loop_bound}%, Difference from Prolex: {abs(percent_complete_prolex-percent_complete_no_loop_bound)}%')

    # Get Completion times for each env
    time_complete_percent = []
    for env in res:
        for task in res[env]:
            if res[env][task]['correct_percent'] == 1.0:
                time_complete_percent.append(res[env][task]['time'])

    # Set up plot arrays
    x_no_loop_bound = []
    y_no_loop_bound = []
    for task in time_complete_percent:
        x_no_loop_bound.append(task)

    x_no_loop_bound.sort()
    num_complete = 0
    for val in x_no_loop_bound:
        num_complete += 1
        y_no_loop_bound.append(float(num_complete)/120*100)

    ###################
    # PROLEX NoSketch #
    ###################

    res = Prolex_NoSketch_data_parser.parse()

    # Get Num Completions accross all envs
    num_complete = 0
    total_num = 0
    for env in res:
        for task in res[env]:
            if res[env][task]['correct_percent'] == 1.0:
                num_complete += 1

            total_num += 1

    percent_complete_no_sketch = float(num_complete)/total_num*100
    print(f'Percent Complete NoSketch: {percent_complete_no_sketch}%, Difference from Prolex: {abs(percent_complete_prolex-percent_complete_no_sketch)}%')

    # Plot
    plt.plot(x_prolex, y_prolex, 'go-', label='Prolex')
    plt.plot(x_no_prune, y_no_prune, 'bo-', label='NoPrune')
    plt.plot(x_no_llm, y_no_llm, 'ro-', label='NoLLM')
    plt.plot(x_sketch_only, y_sketch_only, 'yo-', label='SketchOnly')
    plt.plot(x_no_loop_bound, y_no_loop_bound, 'ko-', label='NoLoopBound')
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Complete (%)')
    plt.show()
