import sys
sys.path.append('../..')
sys.path.append('../../Env')
from dsl import *

"""
Storing groceries

O = Scan("Drawer")
let o = O[0]
action(o,"open")
O1 = Scan("Cereal")
for i1 in O1:
    action(i1, "pick")
    action(i1,"place",o,"Inside")
action(o,"close")
O = Scan("fridge")
let o = O[0]
action(o,"open")
O2 = Scan("Vegetable")
for i2 in O2:
    action(i2, "pick")
    action(i2,"place",o,"Inside")
action(o,"close")
"""

def B9_prog():
    program = Prog(0)
    os1 = object_set()
    sc1 = Scan("Drawer",os1)
    var0 = variable("o1")
    let1 = Let(var0, os1, 0, "Drawer")
    act1 = Act(var0,"Open", "Drawer")
    os2 = object_set()
    sc2 = Scan('Cereal',os2)
    itr0 = Iterator()
    var1 = variable(itr0.pretty_str(0))
    for1 = Foreach_obj(itr0, os2)
    act2 = Act(var1,"Grab", "Cereal")
    act3 = Act(var1, 'Place', "Cereal", [['Inside', var0]])
    for1.add_stmnt(act2)
    for1.add_stmnt(act3)
    act4 = Act(var0, 'Close', "Drawer")

    os3 = object_set()
    sc3 = Scan("Fridge",os3)
    var2 = variable("o2")
    let2 = Let(var2, os3, 0, "Fridge")
    act5 = Act(var2,"Open", "Fridge")
    os4 = object_set()
    sc4 = Scan('Vegetable',os4)
    itr1 = Iterator()
    var3 = variable(itr1.pretty_str(0))
    for2 = Foreach_obj(itr1, os4)
    act6 = Act(var3,"Grab", "Vegetable")
    act7 = Act(var3, 'Place', "Vegetable", [['Inside', var2]])
    for2.add_stmnt(act6)
    for2.add_stmnt(act7)
    act8 = Act(var2, 'Close', "Fridge")
    var = variable("Kitchen_1")
    goto1 = Goto("Goto", var)

    goto1.add_stmnt(sc1)
    goto1.add_stmnt(let1)
    goto1.add_stmnt(act1)
    goto1.add_stmnt(sc2)
    goto1.add_stmnt(for1)
    goto1.add_stmnt(act4)
    goto1.add_stmnt(sc3)
    goto1.add_stmnt(let2)
    goto1.add_stmnt(act5)
    goto1.add_stmnt(sc4)
    goto1.add_stmnt(for2)
    goto1.add_stmnt(act8)

    program.add_stmnt(goto1)

    return program
# prog = B9_prog()
# env = E5()
# trace = prog.execute(env)
# B9_demo_on_E5 = trace[2]
# print(B9_demo_on_E5.pretty_str(1))