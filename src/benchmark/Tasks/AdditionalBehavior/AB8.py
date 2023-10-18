import sys
sys.path.append('../../..')
sys.path.append('/Users/kiar-admin/Dev/Neurosymbolic-policies/')

from dsl import *
#from benchmark.Environments.E import * 



"""
Additional Behavior Task #8 (go to the kitchen, grab all plates and put them inside the sink)
"""

def AB8():
    program = Prog(0)
    # go to kitchen
    k_var = variable('Kitchen_1')
    goto_k = Goto('Goto', k_var)

    # sink
    sink_set = object_set()
    scan_sinks = Scan("Sink", sink_set)
    sink_var = variable("sink_var")
    let1 = Let(sink_var, sink_set, 0, "Sink")
    goto_k.add_stmnt(scan_sinks)
    goto_k.add_stmnt(let1)

    # plates
    plate_set = object_set()
    scan_plates = Scan("Plate", plate_set)
    plate_iter = Iterator()
    i0 = variable(plate_iter.pretty_str(0))
    for1 = Foreach_obj(plate_iter, plate_set)
    grab_clothe_act = Act(i0,"Grab", "Plate")
    place_in_sink_act = Act(i0, "Place", "Plate", [["Inside", sink_var]])
    for1.add_stmnt(grab_clothe_act)
    for1.add_stmnt(place_in_sink_act)

    goto_k.add_stmnt(scan_plates)
    goto_k.add_stmnt(for1)
    program.add_stmnt(goto_k)
    return program



# execute the program on E environment
#prog = AB8()
#env = E()
#trace = prog.execute(env)
#demo = trace[2]
#print (prog.pretty_str())
#print (demo.pretty_str(1))
