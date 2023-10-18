import sys
sys.path.append('../../..')

from dsl import *
from benchmark.Environments.E1 import * 


"""
Survey Task 9 (go to the livingroom; pickup a basket; take it to the bedroom and put it next to the bed; pickup all clothes; put them in the basket)
Goto("Livingroom"):
    O1 = Scan("Basket")
    let o1 = O1[0]
Goto("Bedroom"):
    O2 = Scan("Bed")
    let o2 = O2[0]
    act(o1,"Place",[["Near",o2]])
    O3 = Scan("Clothes")
    for i3 in O3:
        act(i3,"Grab")
        act(i3,"Place",[["Inside",o1]])
"""

def S9():
    program = Prog(0)
    var0 = variable("Livingroom_1")
    goto = Goto('Goto',loc=var0)
    os1 = object_set()
    sc1 = Scan("Basket",os1)
    var1 = variable("o1")
    let1 = Let(var1,os1,0)
    grab_basket = Act(var1, 'Grab', 'Basket')
    var2 = variable("Bedroom_1")
    goto2 = Goto('Goto',var2)
    os2 = object_set()
    sc2 = Scan("Bed",os2)
    var3 = variable("o2")
    let2 = Let(var3,os2,0)
    act1 = Act(var1,"Place",'Basket', [["Near",var3]])
    os3 = object_set()
    sc3 = Scan("Clothes",os3)
    itr0 = Iterator()
    var4 = variable(itr0.pretty_str(0))
    for1 = Foreach_obj(itr0,os3)
    act2 = Act(var4,"Grab")
    act3 = Act(var4,"Place",'Clothes',[["Inside",var1]])
    for1.add_stmnt(act2)
    for1.add_stmnt(act3)
    goto2.add_stmnt(sc2)
    goto2.add_stmnt(let2)
    goto2.add_stmnt(act1)
    goto2.add_stmnt(sc3)
    goto2.add_stmnt(for1)
    goto.add_stmnt(sc1)
    goto.add_stmnt(let1)
    goto.add_stmnt(grab_basket)
    program.add_stmnt(goto)
    program.add_stmnt(goto2)
    return program



# execute the program on an environment
# prog = S9()
# env = E1()
# trace = prog.execute(env)
# demo = trace[2]
# print (prog.pretty_str())
# print (demo.pretty_str(1))