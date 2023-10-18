import sys
sys.path.append('../../..')
sys.path.append('/Users/kiar-admin/Dev/Neurosymbolic-policies/')

from dsl import *
#from benchmark.Environments.E import * 



"""
Additional Behavior Task #9 (go to the livingroom, pickup all trash, take it to the kitchen)
"""

def AB9():
    program = Prog(0)
    # go to livingroom
    lr_var = variable('Livingroom_1')
    goto_lr = Goto('Goto', lr_var)

    # trashs
    trash_set = object_set()
    scan_trashs = Scan("Trash", trash_set)
    trash_iter = Iterator()
    i0 = variable(trash_iter.pretty_str(0))
    for1 = Foreach_obj(trash_iter, trash_set)
    grab_trash_act = Act(i0,"Grab", "Trash")
    for1.add_stmnt(grab_trash_act)

    goto_lr.add_stmnt(scan_trashs)
    goto_lr.add_stmnt(for1)

    # go to kitchen
    k_var = variable('Kitchen_1')
    goto_k = Goto('Goto', k_var)


    program.add_stmnt(goto_lr)

    program.add_stmnt(goto_k)
    return program



# execute the program on E environment
#prog = AB9()
#env = E()
#trace = prog.execute(env)
#demo = trace[2]
#print (prog.pretty_str())
#print (demo.pretty_str(1))
