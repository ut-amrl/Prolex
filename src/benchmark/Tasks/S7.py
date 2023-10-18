import sys
sys.path.append('../../..')

from dsl import *
from benchmark.Environments.E1 import * 


"""
Survey Task 7 (Go to all rooms; pick up any book that is red; come to the living room; put them all on the table)
Goto_each():
    O1 = Scan("Book")
    for i1 in O1:
        if check_prop(i1,"Red"):
            act(i1,"Grab")
Goto("Livingroom"):
    O2 = Scan("Table")
    let o2 = O2[0]
    for i1 in O1:
        act(i1,"Place",[["On",o2]])
"""

def S7_prog():
    program = Prog(0)
    i0 = Iterator()
    gotoe = Goto('Goto_each',itr=i0)
    os1 = object_set()
    sc1 = Scan("Book",os1)
    i1 = Iterator()
    var1 = variable(i1.pretty_str(0))
    for1 = Foreach_obj(i1,os1)
    if1 = If(Bexp('single',Check_prop(var1,"Red")))
    act1 = Act(var1,"Grab","Book")
    var2 = variable("Livingroom_1")
    goto = Goto('Goto',loc=var2)
    os2 = object_set()
    sc2 = Scan("Table",os2)
    var3 = variable("o2")
    let2 = Let(var3,os2,0)
    i2 = Iterator()
    var4 = variable(i2.pretty_str(0))
    for2 = Foreach_obj(i2,os1)
    act2 = Act(var4,"Place","Book",[["On",var3]])
    if1.add_stmnt(act1)
    for1.add_stmnt(if1)
    gotoe.add_stmnt(sc1)
    gotoe.add_stmnt(for1)
    for2.add_stmnt(act2)
    goto.add_stmnt(sc2)
    goto.add_stmnt(let2)
    goto.add_stmnt(for2)
    program.add_stmnt(gotoe)
    program.add_stmnt(goto)
    return program



# execute the program on an environment
# prog = S7()
# env = E1()
# trace = prog.execute(env)
# demo = trace[2]
# print (prog.pretty_str())
# print (demo.pretty_str(1))