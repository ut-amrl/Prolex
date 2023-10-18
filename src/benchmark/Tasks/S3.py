import sys
sys.path.append('../../..')
#sys.path.append('/Users/kiar-admin/Dev/Neurosymbolic-policies/')

from dsl import *
from benchmark.Environments.E1 import * 


"""
Survey Task 3 (go to the living room; 
               grab all objects that are edible; # change to: grab all Matchbox which is also dangerous for children
               put them inside the drawer)
"""

def S3_prog():
    program = Prog(0)
    # go to Livingroom_1
    lr1_var = variable('Livingroom_1')
    goto_lr1 = Goto('Goto', lr1_var)

    # drawer
    drawer_set = object_set()
    scan_drawers = Scan("Drawer", drawer_set)
    drawer_var = variable("drawer_var")
    let1 = Let(drawer_var, drawer_set, 0, "Drawer")
    goto_lr1.add_stmnt(scan_drawers)
    goto_lr1.add_stmnt(let1)

    # mbox
    mbox_set = object_set()
    scan_mboxs = Scan("Matchbox", mbox_set)
    mbox_iter = Iterator()
    i0 = variable(mbox_iter.pretty_str(0))
    for1 = Foreach_obj(mbox_iter, mbox_set)
    grab_mbox_act = Act(i0, "Grab", "Matchbox")
    place_in_drawer_act = Act(i0, "Place", "Matchbox", [["Inside", drawer_var]])
    for1.add_stmnt(grab_mbox_act)
    for1.add_stmnt(place_in_drawer_act)
    goto_lr1.add_stmnt(scan_mboxs)
    goto_lr1.add_stmnt(for1)
    
    program.add_stmnt(goto_lr1)
    return program



# execute the program on an environment
# prog = S3()
# env = E1()
# trace = prog.execute(env)
# demo = trace[2]
# print (prog.pretty_str())
# print (demo.pretty_str(1))