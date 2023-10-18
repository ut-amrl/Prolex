import sys
sys.path.append('../..')
sys.path.append('../../Env')
from dsl import *

"""
Placing fruits from fridge on to kitchen top
O4 = Scan("Countertop")
let o4 = O4[0]
O1 = Scan("Fridge")
let o1 = O1[0]
action(o1,"open")
O2 = Scan("Fruit")
for each i2 in O2:
    action(i2, "Grab")
    action(i2,"place",o4,"On")    
action(o1, "close")
"""

def B2_prog():
    program = Prog(0)
    os1 = object_set()
    sc1 = Scan("Counter",os1)
    os2 = object_set()
    os3 = object_set()
    sc2 = Scan("Fridge", os2)
    var1 = variable("o1")
    let1 = Let(var1,os1,0, "Counter")
    var2 = variable("o2")
    let2 = Let(var2,os2,0, "Fridge")
    act1 = Act(var2, 'Open', "Fridge")
    sc3 = Scan('Fruit', os3)
    itr0 = Iterator()
    i0  = variable(itr0.pretty_str(0))
    for1 = Foreach_obj(itr0,os3)
    act2 = Act(i0,"Grab", 'Fruit')
    act3 = Act(i0, "Place", 'Fruit', [["On", var1]])
    act4 = Act(var2, 'Close', "Fridge")
    for1.add_stmnt(act2)
    for1.add_stmnt(act3)
    var = variable('Kitchen_1')
    goto1 = Goto('Goto', var)

    goto1.add_stmnt(sc1)
    goto1.add_stmnt(sc2)
    goto1.add_stmnt(let1)
    goto1.add_stmnt(let2)
    goto1.add_stmnt(act1)
    goto1.add_stmnt(sc3)
    goto1.add_stmnt(for1)
    goto1.add_stmnt(act4)

    program.add_stmnt(goto1)
    return program
# prog = B2_prog()
# env = E5()
# trace = prog.execute(env)
# B2_demo_on_E5 = trace[2]
# print(B2_demo_on_E5.pretty_str(1))