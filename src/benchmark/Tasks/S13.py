import sys
sys.path.append('../../..')

from dsl import *
from benchmark.Environments.E1 import * 


"""
Survey Task 13 (go to kitchen, open the window if the stove is on)
Goto('Kitchen'):
    O1 = Scan("Window")
    let o1 = O1[0]
    O2 = Scan("Stove")
    let o2 = O2[0]
    if Check_prop(o2,"On"):
        act(o1,'Open')
"""

def S13_prog():
    program = Prog(0)
    var0 = variable('Kitchen_1')
    goto = Goto('Goto',loc=var0)
    os1 = object_set()
    sc1 = Scan("Window",os1)
    var1 = variable("o1")
    let1 = Let(var1,os1,0)
    os2 = object_set()
    sc2 = Scan("Stove",os2)
    var2 = variable("o2")
    let2 = Let(var2,os2,0)
    if1 = If(Bexp('single',Check_prop(var2,'On')))
    act1 = Act(var1,'Open','Window')
    if1.add_stmnt(act1)
    goto.add_stmnt(sc1)
    goto.add_stmnt(let1)
    goto.add_stmnt(sc2)
    goto.add_stmnt(let2)
    goto.add_stmnt(let2)
    goto.add_stmnt(if1)
    program.add_stmnt(goto)
    return program



# execute the program on an environment
# prog = S13()
# env = E1()
# trace = prog.execute(env)
# demo = trace[2]
# print (prog.pretty_str())
# print (demo.pretty_str(1))