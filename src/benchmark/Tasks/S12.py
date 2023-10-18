import sys
sys.path.append('../../..')

from dsl import *
from benchmark.Environments.E1 import * 


"""
Survey Task 12 (go to the living room, find an empty box, go to all rooms, collect books on the beds and put them in the box; take the box back to the livingroom)
Goto('Livingroom'):
    O1 = Scan("Box")
    let o1 = O1[0]
    act(o1,"Grab")
Goto('Bedroom_1'):
    O2 = Scan("Bed")
    let o2 = O2[0]
    O3 = Scan("Book")
    for o3 in O3:
        If Check_rel(o3,o2,"On"):
            act(o3,"Grab")
            act(o3,"Place",[["Inside",o1]])
Goto('Livingroom'):
"""

def S12_prog():
    program = Prog(0)
    var0 = variable('Livingroom_1')
    goto = Goto('Goto',loc=var0)
    os1 = object_set()
    sc1 = Scan('Box',os1)
    var1 = variable("o1")
    let1 = Let(var1,os1,0)
    act1 = Act(var1,"Grab",'Box')
    itr0 = variable('Bedroom_1')
    gotoe = Goto('Goto',loc=itr0)
    os2 = object_set()
    sc2 = Scan("Bed",os2)
    var2 = variable("o2")
    let2 = Let(var2,os2,0)
    os3 = object_set()
    sc3 = Scan('Book',os3)
    itr1 = Iterator()
    var3 = variable(itr1.pretty_str(0))
    for1 = Foreach_obj(itr1,os3)
    if1 = If(Bexp('single',Check_rel(var3,var2,"On")))
    act2 = Act(var3,"Grab",'Book')
    act3 = Act(var3,"Place",'Book',[["Inside",var1]])
    var4 = variable("Livingroom_1")
    goto2 = Goto('Goto',loc=var4)
    if1.add_stmnt(act2)
    if1.add_stmnt(act3)
    for1.add_stmnt(if1)
    gotoe.add_stmnt(sc2)
    gotoe.add_stmnt(let2)
    gotoe.add_stmnt(sc3)
    gotoe.add_stmnt(for1)
    goto.add_stmnt(sc1)
    goto.add_stmnt(let1)
    goto.add_stmnt(act1)
    program.add_stmnt(goto)
    program.add_stmnt(gotoe)
    program.add_stmnt(goto2)
    return program



# execute the program on an environment
# prog = S12()
# env = E1()
# trace = prog.execute(env)
# demo = trace[2]
# print (prog.pretty_str())
# print (demo.pretty_str(1))