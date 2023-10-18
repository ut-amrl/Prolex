import sys
sys.path.append('../../..')
sys.path.append('/Users/kiar-admin/Dev/Neurosymbolic-policies/')

from dsl import *
#from benchmark.Environments.E import * 



"""
Additional Behavior Task #15 (go to each room, grab all bottles, go to the kitchen, empty all bottles)
"""

def AB15():
    program = Prog(0)
    i0 = Iterator()
    var0 = variable(i0.pretty_str(0))
    gotoe = Goto('Goto_each',itr=var0)

    # bottles
    bottle_set = object_set()
    scan_bottles = Scan("Bottle", bottle_set)
    bottle_iter = Iterator()
    i0 = variable(bottle_iter.pretty_str(0))
    gotoe.add_stmnt(scan_bottles)
    for1 = Foreach_obj(bottle_iter, bottle_set)
    for1.add_stmnt(Act(i0, "Grab", "Bottle"))
    gotoe.add_stmnt(for1)
    program.add_stmnt(gotoe)

    # go to kitchen
    k_var = variable('Kitchen_1')
    goto_k = Goto('Goto', k_var)



    # bottles (2nd time, in the kitchen)
    bottle_set = object_set()
    scan_bottles = Scan("Bottle", bottle_set)
    bottle_iter = Iterator()
    i0 = variable(bottle_iter.pretty_str(0))
    gotoe.add_stmnt(scan_bottles)
    for1 = Foreach_obj(bottle_iter, bottle_set)
    for1.add_stmnt(Act(i0, "Empty", "Bottle"))
    goto_k.add_stmnt(for1)


    program.add_stmnt(goto_k)
    return program



# execute the program on E environment
#prog = AB15()
#env = E()
#trace = prog.execute(env)
#demo = trace[2]
#print (prog.pretty_str())
#print (demo.pretty_str(1))
