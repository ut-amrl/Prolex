import sys
sys.path.append('../../..')

from dsl import *
from benchmark.Environments.E1 import * 


"""
Survey Task 8 (go to the living room; pickup any boxes that are near the door; put them on the table)
Goto("Livingroom"):
    O1 = Scan("Door")
    let o1 = O1[0]
    O2 = Scan("Box")
    O3 = Scan("Table")
    let o3 = O3[0]
    for o2 in O2:
        if Check_rel(o2,o1,"near"):
            act(o2, "Grab")
            act(o2, "Place", ["On",o3])
"""

def S8_prog():
    program = Prog(0)
    var0 = variable("Livingroom_1")
    goto = Goto('Goto',loc=var0)
    os1 = object_set()
    sc1 = Scan("Door",os1)
    var2 = variable("o1")
    let1 = Let(var2,os1,0)
    os2 = object_set()
    sc2 = Scan("Box",os2)
    os3 = object_set()
    sc3 = Scan("Table",os3)
    var3 = variable("o3")
    let2 = Let(var3,os3,0)
    itr0 = Iterator()
    var1 = variable(itr0.pretty_str(0))
    for1 = Foreach_obj(itr0, os2)
    if1 = If(Bexp('single',Check_rel(var1,var2,"Near")))
    act1 = Act(var1,"Grab","Box")
    act2 = Act(var1,"Place","Box",[["On",var3]])
    if1.add_stmnt(act1)
    if1.add_stmnt(act2)
    for1.add_stmnt(if1)
    goto.add_stmnt(sc1)
    goto.add_stmnt(let1)
    goto.add_stmnt(sc2)
    goto.add_stmnt(sc3)
    goto.add_stmnt(let2)
    goto.add_stmnt(for1)
    program.add_stmnt(goto)
    return program



# execute the program on an environment
# prog = S8()
# env = E1()
# trace = prog.execute(env)
# demo = trace[2]
# print (prog.pretty_str())
# print (demo.pretty_str(1))