import sys
sys.path.append('../..')
sys.path.append('../../Env')
from dsl import *

"""
Boxing books for storage
O1 = Scan("Book")
O2 = Scan("Box")
let o = O2[0]
for each i1 in O1:
    action(i1,"pick")
    action(i1,"place",o,"Inside")
"""

def B3_prog():
    program = Prog(0)
    os1 = object_set()
    sc1 = Scan("Book",os1)
    os2 = object_set()
    sc2 = Scan("Box", os2)
    var = variable("o")
    let1 = Let(var,os2,0, "Box")
    itr0 = Iterator()
    i0  = variable(itr0.pretty_str(0))
    for1 = Foreach_obj(itr0,os1)
    act1 = Act(i0,"Grab", "Book")
    act2 = Act(i0,"Place", "Book", [["Inside", var]])
    for1.add_stmnt(act1)
    for1.add_stmnt(act2)
    var = variable("Livingroom_1")
    goto1 = Goto("Goto", var)

    goto1.add_stmnt(sc1)
    goto1.add_stmnt(sc2)
    goto1.add_stmnt(let1)
    goto1.add_stmnt(for1)

    program.add_stmnt(goto1)

    return program
# prog = B3_prog()
# env = E1()
# trace = prog.execute(env)
# B3_demo_on_E1 = trace[2]
# print(B3_demo_on_E1.pretty_str(1))