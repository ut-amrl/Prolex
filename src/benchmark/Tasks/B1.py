import sys
sys.path.append('../..')
sys.path.append('../../Env')
from dsl import *

"""
Sorting books
O1 = Scan("book")
O2 = Scan("drawer")
let o1 = O2[0]
let o2 = O2[1]
action(o1, "Open")
action(o2, "Open")
for each i1 in O1:
    if Check_prop_pred(i1,"red"):
        action(i1,"Grab")
        action(i1,"place",o1,"on")
    if Check_prop_pred(i1,"white"):
        action(i1,"Grab")
        action(i1,"place",o2,"on")
action(o1, "Close")
action(o2, "Close")
"""

def B1_prog():
    program = Prog(0)
    os1 = object_set()
    sc1 = Scan("Book",os1)
    os2 = object_set()
    sc2 = Scan("Drawer", os2)
    var1 = variable("o1")
    let1 = Let(var1,os2,0, "Drawer")
    var2 = variable("o2")
    let2 = Let(var2,os2,1, "Drawer")
    act5 = Act(var1, "Open", "Drawer")
    act7 = Act(var2, "Open", "Drawer")
    act6 = Act(var1, "Close", "Drawer")
    act8 = Act(var2, "Close", "Drawer")
    itr0 = Iterator()
    i0  = variable(itr0.pretty_str(0))
    for1 = Foreach_obj(itr0,os1)
    act1 = Act(i0,"Grab", "Book")
    act2 = Act(i0, "Place", "Book", [["Inside", var1]])
    for1.add_stmnt(act1)
    if2 = If(Bexp('single', Check_prop(i0, "White", "Book")))
    if2.add_stmnt(act2)
    if3 = If(Bexp('single', Check_prop(i0, "Red", "Book")))
    act3 = Act(i0, "Place", "Book", [["Inside", var2]])
    if3.add_stmnt(act3)
    for1.add_stmnt(if2)
    for1.add_stmnt(if3)
    var = variable('Livingroom_1')
    goto1 = Goto('Goto', var)

    goto1.add_stmnt(sc1)
    goto1.add_stmnt(sc2)
    goto1.add_stmnt(let1)
    goto1.add_stmnt(let2)
    goto1.add_stmnt(act5)
    goto1.add_stmnt(act7)
    goto1.add_stmnt(for1)
    goto1.add_stmnt(act6)
    goto1.add_stmnt(act8)

    program.add_stmnt(goto1)
    return program
# prog = B1_prog()
# env = E1()
# trace = prog.execute(env)
# B1_demo_on_E1 = trace[2]
# print(B1_demo_on_E1.pretty_str(1))