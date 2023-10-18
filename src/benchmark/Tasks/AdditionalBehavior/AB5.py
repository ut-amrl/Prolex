import sys
sys.path.append('../../..')
sys.path.append('/Users/kiar-admin/Dev/Neurosymbolic-policies/')

from dsl import *
#from benchmark.Environments.E import * 



"""
Additional Behavior Task #5 (go to the kitchen, clean all fruits)
"""

def AB5():
    program = Prog(0)
    # go to kitchen
    k_var = variable('Kitchen_1')
    goto_k = Goto('Goto', k_var)

    # fruits
    fruit_set = object_set()
    scan_fruits = Scan("Fruit", fruit_set)
    fruit_iter = Iterator()
    i0 = variable(fruit_iter.pretty_str(0))
    for1 = Foreach_obj(fruit_iter, fruit_set)
    for1.add_stmnt(Act(i0, "Clean", "Fruit"))

    goto_k.add_stmnt(scan_fruits)
    goto_k.add_stmnt(for1)

    program.add_stmnt(goto_k)
    return program




# execute the program on E environment
#prog = AB5()
#env = E()
#trace = prog.execute(env)
#demo = trace[2]
#print (prog.pretty_str())
#print (demo.pretty_str(1))
