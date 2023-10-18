def parse():
    with open('False.txt', 'r') as f:
        lines = f.readlines()

    env_diffs = ['e', 'm', 'h']
    env_iter = -1

    task_names = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'S0', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12', 'S13', 'S14', 'AB1', 'AB2', 'AB3', 'AB4', 'AB5', 'AB6', 'AB7', 'AB8', 'AB9', 'AB10', 'AB11', 'AB12', 'AB13', 'AB14', 'AB15']

    task_iter = 0

    task_dict = {}
    env_dict = {}
    for line in lines:
        if line == 'ROW\n':
            if env_iter == -1:
                env_iter += 1
            else:
                env_dict[env_diffs[env_iter]] = task_dict
                env_iter += 1

                #Reset task counters
                task_dict = {}
                task_iter = 0
        elif task_iter == len(task_names):
            # On last row
            assert env_iter == 2
            env_dict[env_diffs[env_iter]] = task_dict
            break
        else:
            temp_line = line.strip('\n')
            temp_dict = dict(eval(temp_line))
            task_dict[task_names[task_iter]] = temp_dict
            task_iter += 1

    return env_dict
