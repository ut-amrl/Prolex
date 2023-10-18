import sys
sys.path.append('../../..')
sys.path.append('/Users/kiar-admin/Dev/Neurosymbolic-policies/')

from dsl import *
#from benchmark.Environments.E import * 



"""
Additional Behavior Task #4 (go to the kitchen, put all empty mugs into the sink)
"""



def AB4():
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

    # mugs
    mug_set = object_set()
    scan_mugs = Scan("Mug", mug_set)
    mug_iter = Iterator()
    i0 = variable(mug_iter.pretty_str(0))
    for1 = Foreach_obj(mug_iter, mug_set)

    if_full = If(Bexp('neg',Check_prop(i0,"Full", "Mug")))
    if_full.add_stmnt(Act(i0, "Grab", "Mug"))
    if_full.add_stmnt(Act(i0, "Place", 'Mug', [["Inside", sink_var]]))
    
    for1.add_stmnt(if_full)


    goto_k.add_stmnt(scan_mugs)
    goto_k.add_stmnt(for1)
    program.add_stmnt(goto_k)
    return program



# execute the program on E environment
#prog = AB4()
#env = E()
#trace = prog.execute(env)
#demo = trace[2]
#print (prog.pretty_str())
#print (demo.pretty_str(1))
