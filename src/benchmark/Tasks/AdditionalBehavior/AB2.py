import sys
sys.path.append('../../..')
sys.path.append('/Users/kiar-admin/Dev/Neurosymbolic-policies/')

from dsl import *
#from benchmark.Environments.E import * 



"""
Additional Behavior Task #2 (go to the kitchen put the dirty Plates in the dishwasher)
"""

def AB2():
    program = Prog(0)

    # go to kitchen
    k_var = variable('Kitchen_1')
    goto_k = Goto('Goto', k_var)

    # dishwasher
    dw_set = object_set()
    scan_dws = Scan("Dishwasher", dw_set)
    dw_var = variable("dw_var")
    let1 = Let(dw_var, dw_set, 0, "Dishwasher")
    goto_k.add_stmnt(scan_dws)
    goto_k.add_stmnt(let1)
    
    # plates
    plate_set = object_set()
    scan_plates = Scan("Plate", plate_set)
    plate_iter = Iterator()
    i0 = variable(plate_iter.pretty_str(0))
    for1 = Foreach_obj(plate_iter, plate_set)
        
    if_dirty = If(Bexp('neg',Check_prop(i0,"Clean", "Plate")))
    if_dirty.add_stmnt(Act(i0, "Grab", "Plate"))
    if_dirty.add_stmnt(Act(i0, "Place", 'Plate', [["Inside", dw_var]]))
    
    for1.add_stmnt(if_dirty)
    goto_k.add_stmnt(scan_plates)
    goto_k.add_stmnt(for1)

    program.add_stmnt(goto_k)
    return program

# execute the program on E environment
#prog = AB2()
#env = E()
#trace = prog.execute(env)
#demo = trace[2]
#print (prog.pretty_str())
#print (demo.pretty_str(1))
