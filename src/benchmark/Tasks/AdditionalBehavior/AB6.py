import sys
sys.path.append('../../..')
sys.path.append('/Users/kiar-admin/Dev/Neurosymbolic-policies/')

from dsl import *
#from benchmark.Environments.E import * 



"""
Additional Behavior Task #6 (go to the kitchen, grab a cleaning tool, clean all windows)
"""

def AB6():
    program = Prog(0)

    # go to kitchen
    k_var = variable('Kitchen_1')
    goto_k = Goto('Goto', k_var)


    # cleaner
    cleaner_set = object_set()
    scan_cleaneres = Scan("Cleaning", cleaner_set)
    cleaner_var = variable("cleaner_var")
    let1 = Let(cleaner_var, cleaner_set, 0, "Cleaning")
    goto_k.add_stmnt(scan_cleaneres)
    goto_k.add_stmnt(let1)
    goto_k.add_stmnt(Act(cleaner_var, "Grab"))

    # windows
    window_set = object_set()
    scan_windows = Scan("Window", window_set)
    window_iter = Iterator()
    i0 = variable(window_iter.pretty_str(0))
    for1 = Foreach_obj(window_iter, window_set)
    for1.add_stmnt(Act(i0, "Clean", "Window"))

    goto_k.add_stmnt(scan_windows)
    goto_k.add_stmnt(for1)
    program.add_stmnt(goto_k)
    return program



# execute the program on E environment
#prog = AB6()
#env = E()
#trace = prog.execute(env)
#demo = trace[2]
#print (prog.pretty_str())
#print (demo.pretty_str(1))
