from data_parsers import Prolex_data_parser

import matplotlib.pyplot as plt

if __name__ == '__main__':
    res = Prolex_data_parser.parse()

    # Get Num Completions accross all envs
    num_complete = 0
    total_num = 0
    for task in res['h']:
        if res['h'][task]['correct_percent'] == 1.0:
            num_complete += 1

        total_num += 1

    print(f'Percent Complete (Largest AST Batch): {float(num_complete)/total_num*100}%')

    # Get Completion times for each env
    time_complete_percent_all = {}
    for env in res:
        time_complete_percent = []
        num_complete = 0
        for task in res[env]:
            if res[env][task]['correct_percent'] == 1.0:
                num_complete += 1
                time_complete_percent.append(res[env][task]['time'])

        time_complete_percent_all[env] = time_complete_percent

    # Easy
    xe = []
    ye = []
    for task in time_complete_percent_all['e']:
        xe.append(task)

    xe.sort()
    num_complete = 0
    for val in xe:
        num_complete += 1
        ye.append(float(num_complete)/40*100)
    
    # Medium
    xm = []
    ym = []
    for task in time_complete_percent_all['m']:
        xm.append(task)

    xm.sort()
    num_complete = 0
    for val in xm:
        num_complete += 1
        ym.append(float(num_complete)/40*100)
    
    # Hard
    xh = []
    yh = []
    for task in time_complete_percent_all['h']:
        xh.append(task)

    xh.sort()
    num_complete = 0
    for val in xh:
        num_complete += 1
        yh.append(float(num_complete)/40*100)
   
    plt.bar('[11,23]', ye[-1])
    plt.bar('[24,35]', ym[-1])
    plt.bar('[36,72]', yh[-1])
    plt.xlabel('Time (s)')
    plt.ylabel('Complete (%)')
    plt.show()
