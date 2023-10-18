import sys
sys.path.append('../../..')
sys.path.append('/Users/kiar-admin/Dev/Neurosymbolic-policies/')

from dsl import *
#from benchmark.Environments.E import * 



"""
Additional Behavior Task #3 (go to the kitchen and clean all Plates)
"""

def AB3():
    program = Prog(0)

    # go to kitchen
    k_var = variable('Kitchen_1')
    goto_k = Goto('Goto', k_var)

    # plates
    plate_set = object_set()
    scan_plates = Scan("Plate", plate_set)
    plate_iter = Iterator()
    i0 = variable(plate_iter.pretty_str(0))
    for1 = Foreach_obj(plate_iter, plate_set)
    for1.add_stmnt(Act(i0, "Clean", "Plate"))

    goto_k.add_stmnt(scan_plates)
    goto_k.add_stmnt(for1)

    program.add_stmnt(goto_k)
    return program



# execute the program on E environment
#prog = AB3()
#env = E()
#trace = prog.execute(env)
#demo = trace[2]
#print (prog.pretty_str())
#print (demo.pretty_str(1))
