import sys
sys.path.append('../..')
sys.path.append('../../Env')
from dsl import *

"""
Locking every door
Goto_each(li in L):
    O1 = Scan("door")
    for each i1 in O1:
        if check_prop(i1, "open"):
            action(i1, "close")
"""

def B6_prog():
    program = Prog(0)
    itr1 = Iterator()
    goto = Goto('Goto_each',itr=itr1)
    os1 = object_set()
    sc1 = Scan("Door",os1)
    itr0 = Iterator()
    var0 = variable(itr0.pretty_str(0))
    for1 = Foreach_obj(itr0,os1)
    if1 = If(Bexp('single',Check_prop(var0,"Open", "Door")))
    act1 = Act(var0,"Close", "Door")
    if1.add_stmnt(act1)
    for1.add_stmnt(if1)
    goto.add_stmnt(sc1)
    goto.add_stmnt(for1)
    program.add_stmnt(goto)

    return program
# prog = B6_prog()
# env = E1()
# trace = prog.execute(env)
# B6_demo_on_E1 = trace[2]
# print(B6_demo_on_E1.pretty_str(1))