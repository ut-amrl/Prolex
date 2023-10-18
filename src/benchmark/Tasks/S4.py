import sys
sys.path.append('../../..')
#sys.path.append('/Users/kiar-admin/Dev/Neurosymbolic-policies/')

from dsl import *
from benchmark.Environments.E import * 


"""
Survey Task 4 (go to the kitchen; 
              grab all plates and mugs in the dishwasher; 
              put the plates on the sink; 
              put the mugs inside the drawer)
"""

def S4_prog():
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

    # sink
    sink_set = object_set()
    scan_sinks = Scan("Sink", sink_set)
    sink_var = variable("sink_var")
    let1 = Let(sink_var, sink_set, 0, "Dishwasher")
    goto_k.add_stmnt(scan_sinks)
    goto_k.add_stmnt(let1)

    # drawer
    drawer_set = object_set()
    scan_drawers = Scan("Drawer", drawer_set)
    drawer_var = variable("drawer_var")
    let1 = Let(drawer_var, drawer_set, 0, "Drawer")
    goto_k.add_stmnt(scan_drawers)
    goto_k.add_stmnt(let1)

    # plates
    plate_set = object_set()
    scan_plates = Scan("Plate", plate_set)
    plate_iter = Iterator()
    i0 = variable(plate_iter.pretty_str(0))
    for1 = Foreach_obj(plate_iter, plate_set)
    if_in_washer = If(Bexp('single',Check_rel(i0,dw_var,"Inside", "Plate", "Dishwasher")))
    if_in_washer.add_stmnt(Act(i0, "Grab", "Plate"))
    if_in_washer.add_stmnt(Act(i0, "Place", "Plate", [["Inside", sink_var]]))
    for1.add_stmnt(if_in_washer)
    goto_k.add_stmnt(scan_plates)
    goto_k.add_stmnt(for1)

    # mugs
    mug_set = object_set()
    scan_mugs = Scan("Mug", mug_set)
    mug_iter = Iterator()
    i1 = variable(mug_iter.pretty_str(0))
    for2 = Foreach_obj(mug_iter, mug_set)
    if_in_washer = If(Bexp('single',Check_rel(i1,dw_var,"Inside", "Mug", "Dishwasher")))
    if_in_washer.add_stmnt(Act(i1, "Grab", "Mug"))
    if_in_washer.add_stmnt(Act(i1, "Place", "Mug", [["Inside", drawer_var]]))
    for2.add_stmnt(if_in_washer)
    goto_k.add_stmnt(scan_mugs)
    goto_k.add_stmnt(for2)

    program.add_stmnt(goto_k)
    return program



# execute the program on an environment
# prog = S4()
# env = E()
# trace = prog.execute(env)
# demo = trace[2]
# print (prog.pretty_str())
# print (demo.pretty_str(1))