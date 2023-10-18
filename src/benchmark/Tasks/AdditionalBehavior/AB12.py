import sys
sys.path.append('../../..')
sys.path.append('/Users/kiar-admin/Dev/Neurosymbolic-policies/')

from dsl import *
#from benchmark.Environments.E import * 



"""
Additional Behavior Task #12 (go to the bedroom, grab all lights that are off, put them on bed)
"""

def AB12():
    program = Prog(0)
    # go to bedroom
    br_var = variable('Bedroom_1')
    goto_br = Goto('Goto', br_var)    

    # bed
    bed_set = object_set()
    scan_beds = Scan("Bed", bed_set)
    bed_var = variable("bed_var")
    let_bed = Let(bed_var, bed_set, 0, "Bed")
    goto_br.add_stmnt(scan_beds)
    goto_br.add_stmnt(let_bed)

    # lamps
    lamp_set = object_set()
    scan_lamps = Scan("Lamp", lamp_set)
    lamp_iter = Iterator()
    i0 = variable(lamp_iter.pretty_str(0))
    goto_br.add_stmnt(scan_lamps)
    for1 = Foreach_obj(lamp_iter, lamp_set)
    
    if_spoiled = If(Bexp('neg',Check_prop(i0,"On", "Lamp")))
    if_spoiled.add_stmnt(Act(i0, "Grab", "Lamp"))
    if_spoiled.add_stmnt(Act(i0, "Place", 'Lamp', [["On", bed_var]]))
    for1.add_stmnt(if_spoiled)

    goto_br.add_stmnt(for1)
    program.add_stmnt(goto_br)
    return program



# execute the program on E environment
#prog = AB12()
#env = E()
#trace = prog.execute(env)
#demo = trace[2]
#print (prog.pretty_str())
#print (demo.pretty_str(1))
