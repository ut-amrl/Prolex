import sys
sys.path.append('../../..')
sys.path.append('/Users/kiar-admin/Dev/Neurosymbolic-policies/')

from dsl import *
#from benchmark.Environments.E import * 



"""
Additional Behavior Task #1 (go to the kitchen, grab the brush, clean the stove)
"""

def AB1():
    program = Prog(0)

    # go to kitchen
    k_var = variable('Kitchen_1')
    goto_k = Goto('Goto', k_var)

    # brush
    brush_set = object_set()
    scan_brushes = Scan("Brush", brush_set)
    brush_var = variable("brush_var")
    let1 = Let(brush_var, brush_set, 0, "Brush")
    goto_k.add_stmnt(scan_brushes)
    goto_k.add_stmnt(let1)
    goto_k.add_stmnt(Act(brush_var, "Grab"))

    # Stove
    stove_os = object_set()
    stove_scan = Scan("Stove", stove_os)
    stove_iter = Iterator()
    stove_var = variable(stove_iter.pretty_str(0))
    for1 = Foreach_obj(stove_iter, stove_os)
    act1 = Act(stove_var, "Clean")
    
    for1.add_stmnt(act1)
    goto_k.add_stmnt(stove_scan)
    goto_k.add_stmnt(for1)
    program.add_stmnt(goto_k)
    return program



# execute the program on E environment
#prog = AB1()
#env = E()
#trace = prog.execute(env)
#demo = trace[2]
#print (prog.pretty_str())
#print (demo.pretty_str(1))
