import sys
sys.path.append('../..')
sys.path.append('../../Env')
from dsl import *

"""
Brushing lint off clothing
O1 = Scan("brush")
O4 = Scan("Drawer")
let o1 = O1[0]
let o4 = O4[0]
action(o4,"open")
action(o1,"pick")
O2 = Scan("clothes")
O3 = Scan("bed")
let o2 = O3[0]
for each i1 in O2:
    action(i1,"clean") #### Ensure that brush is in your hand
    action(i1, "grab")
    action(i1,"place",o2,"On")
action(o1,"place",o4,"On")
action(o4,"close")
"""

def B5_prog():
    program = Prog(0)
    os1 = object_set()
    sc1 = Scan("Brush", os1)
    os2 = object_set()
    sc2 = Scan("Drawer", os2)
    var1 = variable("o1")
    let1 = Let(var1, os1, 0, "Brush")
    var2 = variable("o2")
    let2 = Let(var2, os2, 0, "Drawer")
    act1 = Act(var2, "Open", "Drawer")
    act2 = Act(var1, "Grab", "Brush")
    os3 = object_set()
    os4 = object_set()
    sc3 = Scan("Clothes", os3)
    sc4 = Scan("Bed", os4)
    var3 = variable("o3")
    let3 = Let(var3, os4, 0, "Bed")
    itr0 = Iterator()
    i0 = variable(itr0.pretty_str(0))
    for1 = Foreach_obj(itr0, os3)
    act3 = Act(i0, "Clean", "Clothes")
    act7 = Act(i0, "Grab", "Clothes")
    act4 = Act(i0, "Place", "Clothes", [["On", var3]])
    act5 = Act(var1, "Place", "Brush", [["Inside", var2]])
    act6 = Act(var2, "Close", "Drawer")
    for1.add_stmnt(act3)
    for1.add_stmnt(act7)
    for1.add_stmnt(act4)
    var = variable('Bedroom_1')
    goto1 = Goto('Goto',var)

    goto1.add_stmnt(sc1)
    goto1.add_stmnt(sc2)
    goto1.add_stmnt(let1)
    goto1.add_stmnt(let2)
    goto1.add_stmnt(act1)
    goto1.add_stmnt(act2)
    goto1.add_stmnt(sc3)
    goto1.add_stmnt(sc4)
    goto1.add_stmnt(let3)
    goto1.add_stmnt(for1)
    goto1.add_stmnt(act5)
    goto1.add_stmnt(act6)

    program.add_stmnt(goto1)

    return program
# prog = B5_prog()
# env = E4()
# trace = prog.execute(env)
# B5_demo_on_E4 = trace[2]
# print(B5_demo_on_E4.pretty_str(1))