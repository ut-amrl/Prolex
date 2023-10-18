import sys
sys.path.append('../../..')
sys.path.append('/Users/kiar-admin/Dev/Neurosymbolic-policies/')

from dsl import *
#from benchmark.Environments.E import * 



"""
Additional Behavior Task #14 (go to all rooms, close all windows)
"""

def AB14():
    program = Prog(0)
    i0 = Iterator()
    var0 = variable(i0.pretty_str(0))
    gotoe = Goto('Goto_each',itr=var0)

    # windows
    window_set = object_set()
    scan_windows = Scan("Window", window_set)
    window_iter = Iterator()
    i0 = variable(window_iter.pretty_str(0))
    gotoe.add_stmnt(scan_windows)
    for1 = Foreach_obj(window_iter, window_set)
    for1.add_stmnt(Act(i0, "Close", "Window"))
    gotoe.add_stmnt(for1)

    program.add_stmnt(gotoe)
    return program



# execute the program on E environment
#prog = AB14()
#env = E()
#trace = prog.execute(env)
#demo = trace[2]
#print (prog.pretty_str())
#print (demo.pretty_str(1))
