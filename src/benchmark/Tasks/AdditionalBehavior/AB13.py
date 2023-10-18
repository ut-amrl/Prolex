import sys
sys.path.append('../../..')
sys.path.append('/Users/kiar-admin/Dev/Neurosymbolic-policies/')

from dsl import *
#from benchmark.Environments.E import * 



"""
Additional Behavior Task #13 (go to all rooms, close all doors)
"""

def AB13():
    program = Prog(0)
    i0 = Iterator()
    var0 = variable(i0.pretty_str(0))
    gotoe = Goto('Goto_each',itr=var0)

    # doors
    door_set = object_set()
    scan_doors = Scan("Door", door_set)
    door_iter = Iterator()
    i0 = variable(door_iter.pretty_str(0))
    gotoe.add_stmnt(scan_doors)
    for1 = Foreach_obj(door_iter, door_set)
    for1.add_stmnt(Act(i0, "Close", "Door"))
    gotoe.add_stmnt(for1)

    program.add_stmnt(gotoe)
    return program



# execute the program on E environment
#prog = AB13()
#env = E()
#trace = prog.execute(env)
#demo = trace[2]
#print (prog.pretty_str())
#print (demo.pretty_str(1))
