import sys
sys.path.append('../../..')

from dsl import *
from benchmark.Environments.E1 import * 


"""
Survey Task 6 
(pickup a basket from the livingroom; go to each room; if there is a bed and there is a pillow in bed; grab the pillow)
Goto("Livingroom"):
    O1=Scan("Basket")
    let o1 = O1[0]
    Goto_each():
        O2 = Scan("Bed")
        Let o2 = O2[0]
        O3 = Scan("Pillow")
        for each i3 in O3:
            If Check_rel(i3,o2,"On"):
                act(i3,"Grab")
                act(i3,"Place",[["Inside",o1]])
"""

def S6():
    program = Prog(0)
    var0 =variable("Livingroom_1")
    goto = Goto('Goto',loc=var0)
    os1 = object_set()
    sc1 = Scan("Basket",os1)
    var1 = variable("o1")
    let1 = Let(var1,os1,0)
    grab_basket = Act(var1, 'Grab', 'Basket')
    var2 = variable('Bedroom_1')
    gotoe = Goto('Goto',loc=var2)
    os2 = object_set()
    sc2 = Scan("Bed",os2)
    var3 = variable("o2")
    let2 = Let(var3,os2,0)
    os3 = object_set()
    sc3 = Scan("Pillow",os3)
    i1 = Iterator()
    var4 = variable(i1.pretty_str(0))
    for1 = Foreach_obj(i1,os3)
    if1 = If(Bexp('single',Check_rel(var4,var3,"On", 'Pillow', 'Bed')))
    act1 = Act(var4,"Grab", 'Pillow')
    act2 = Act(var4,"Place",'Pillow', [["Inside",var1]])
    if1.add_stmnt(act1)
    if1.add_stmnt(act2)
    for1.add_stmnt(if1)
    gotoe.add_stmnt(sc2)
    gotoe.add_stmnt(let2)
    gotoe.add_stmnt(sc3)
    gotoe.add_stmnt(for1)
    goto.add_stmnt(sc1)
    goto.add_stmnt(let1)
    goto.add_stmnt(grab_basket)
    program.add_stmnt(goto)
    program.add_stmnt(gotoe)
    return program



# execute the program on an environment
# prog = S6()
# env = E1()
# trace = prog.execute(env)
# demo = trace[2]
# print (prog.pretty_str())
# print (demo.pretty_str(1))
