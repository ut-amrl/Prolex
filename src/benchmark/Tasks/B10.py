import sys
sys.path.append('../..')
sys.path.append('../../Env')
from dsl import *

"""
Transfer lamps near door to bed
Goto('bedroom'):
    O1 = Scan("lamp")
    O2 = Scan("door")
    let o2 = O2[0])
    O3 = Scan("Bed")
    let o3 = O3[0]
    for each i0 in O1:
        if check_rel(i0,o2,"near"):
            action(i0, "Grab")
            action(i0, "Place", [["Near",o3]])
"""

def B10_prog():
    program = Prog(0)
    r_var = variable("Bedroom_1")
    goto = Goto('Goto', r_var)
    os1 = object_set()
    sc1 = Scan("Lamp",os1)
    os2 = object_set()
    sc2 = Scan("Door",os2)
    var0 = variable("o2")
    let1 = Let(var0,os2,0, "Door")
    os3 = object_set()
    sc3 = Scan("Bed",os3)
    var1 = variable("o3")
    let2 = Let(var1,os3,0, "Bed")
    itr0 = Iterator()
    var2 = variable(itr0.pretty_str(0))
    for1 = Foreach_obj(itr0, os1)
    if1 = If(Bexp('single',Check_rel(var2, var0, "Near", "Lamp", "Door")))
    act1 = Act(var2, "Grab", "Lamp")
    act2 = Act(var2, "Place", "Lamp", [["Near", var1]])
    if1.add_stmnt(act1)
    if1.add_stmnt(act2)
    for1.add_stmnt(if1)
    goto.add_stmnt(sc1)
    goto.add_stmnt(sc2)
    goto.add_stmnt(let1)
    goto.add_stmnt(sc3)
    goto.add_stmnt(let2)
    goto.add_stmnt(for1)
    program.add_stmnt(goto)
    return program
# prog = B10_prog()
# env = E4()
# trace = prog.execute(env)
# B10_demo_on_E4 = trace[2]
# print(B10_demo_on_E4.pretty_str(1))