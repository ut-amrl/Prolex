import sys
sys.path.append('../../..')
sys.path.append('/Users/kiar-admin/Dev/Neurosymbolic-policies/')

from dsl import *
#from benchmark.Environments.E import * 



"""
Additional Behavior Task #7 (go to the bedroom, put all clothes into the drawer)
"""



def AB7():
    program = Prog(0)
    # go to bedroom
    b_var = variable('Bedroom_1')
    goto_b = Goto('Goto', b_var)

    # drawer
    drawer_set = object_set()
    scan_drawers = Scan("Drawer", drawer_set)
    drawer_var = variable("drawer_var")
    let1 = Let(drawer_var, drawer_set, 0, "Drawer")
    goto_b.add_stmnt(scan_drawers)
    goto_b.add_stmnt(let1)
    goto_b.add_stmnt(Act(drawer_var, "Open", "Drawer"))

    # clothes
    clothe_set = object_set()
    scan_clothes = Scan("Clothes",clothe_set)
    cloth_iter = Iterator()
    i0  = variable(cloth_iter.pretty_str(0))
    for1 = Foreach_obj(cloth_iter,clothe_set)
    grab_clothe_act = Act(i0,"Grab", "Clothes")
    place_in_drawer_act = Act(i0, "Place", "Clothes", [["Inside", drawer_var]])
    for1.add_stmnt(grab_clothe_act)
    for1.add_stmnt(place_in_drawer_act)


    goto_b.add_stmnt(scan_clothes)
    goto_b.add_stmnt(for1)
    goto_b.add_stmnt(Act(drawer_var, "Close", "Drawer"))


    program.add_stmnt(goto_b)
    return program



# execute the program on E environment
#prog = AB7()
#env = E()
#trace = prog.execute(env)
#demo = trace[2]
#print (prog.pretty_str())
#print (demo.pretty_str(1))
