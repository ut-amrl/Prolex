import sys
sys.path.append('../../..')
sys.path.append('/Users/kiar-admin/Dev/Neurosymbolic-policies/')

from dsl import *
#from benchmark.Environments.E import * 



"""
Additional Behavior Task #10 (Go to the kitchen, clean the floor)
"""

def AB10():
    program = Prog(0)
    # go to kitchen
    k_var = variable('Kitchen_1')
    goto_k = Goto('Goto', k_var)

    # floor
    floor_set = object_set()
    scan_floors = Scan("Floor", floor_set)
    floor_var = variable("floor_var")
    let1 = Let(floor_var, floor_set, 0, "Floor")
    goto_k.add_stmnt(scan_floors)
    goto_k.add_stmnt(let1)


    # cleaner
    cleaner_set = object_set()
    scan_cleaners = Scan("Cleaning", cleaner_set)
    cleaner_var = variable("cleaner_var")
    let2 = Let(cleaner_var, cleaner_set, 0, "Cleaning")
    goto_k.add_stmnt(scan_cleaners)
    goto_k.add_stmnt(let2)

    goto_k.add_stmnt(Act(cleaner_var,"Grab", "Cleaning"))
    goto_k.add_stmnt(Act(floor_var,"Clean", "Floor"))

    program.add_stmnt(goto_k)
    return program



# execute the program on E environment
#prog = AB10()
#env = E()
#trace = prog.execute(env)
#demo = trace[2]
#print (prog.pretty_str())
#print (demo.pretty_str(1))
