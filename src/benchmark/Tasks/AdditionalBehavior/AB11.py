import sys
sys.path.append('../../..')
sys.path.append('/Users/kiar-admin/Dev/Neurosymbolic-policies/')

from dsl import *
#from benchmark.Environments.E import * 



"""
Additional Behavior Task #11 (go to the kitchen, open the fridge grab spoiled fruits, put them in the sink)
"""

def AB11():
    program = Prog(0)

    # go to kitchen
    k_var = variable('Kitchen_1')
    goto_k = Goto('Goto', k_var)
    
    # fridge
    fridge_set = object_set()
    scan_fridgees = Scan("Fridge", fridge_set)
    fridge_var = variable("fridge_var")
    let1 = Let(fridge_var, fridge_set, 0, "Fridge")
    goto_k.add_stmnt(scan_fridgees)
    goto_k.add_stmnt(let1)
    goto_k.add_stmnt(Act(fridge_var, "Open"))

    # sink
    sink_set = object_set()
    scan_sinks = Scan("Sink", sink_set)
    sink_var = variable("sink_var")
    let2 = Let(sink_var, sink_set, 0, "Sink")
    goto_k.add_stmnt(scan_sinks)
    goto_k.add_stmnt(let2)


    # fruits
    fruit_set = object_set()
    scan_fruits = Scan("Fruit", fruit_set)
    fruit_iter = Iterator()
    i0 = variable(fruit_iter.pretty_str(0))
    for1 = Foreach_obj(fruit_iter, fruit_set)

    if_spoiled = If(Bexp('single',Check_prop(i0,"Spoil", "Fruit")))
    if_spoiled.add_stmnt(Act(i0, "Grab", "Fruit"))
    if_spoiled.add_stmnt(Act(i0, "Place", 'Fruit', [["Inside", sink_var]]))
    for1.add_stmnt(if_spoiled)

    goto_k.add_stmnt(scan_fruits)
    goto_k.add_stmnt(for1)
    program.add_stmnt(goto_k)
    return program


# execute the program on E environment
#prog = AB11()
#env = E()
#trace = prog.execute(env)
#demo = trace[2]
#print (prog.pretty_str())
#print (demo.pretty_str(1))
