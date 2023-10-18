import sys
sys.path.append('../../..')

from dsl import *
from benchmark.Environments.E1 import * 


"""
Survey Task 5 (go to all rooms and turn off the lamps)
Goto_each():
    O1 = Scan("Lamp")
    for each i1 in O1:
        act(i1,"Off")
"""

def S5_prog():
    program = Prog(0)
    i0 = Iterator()
    var0 = variable(i0.pretty_str(0))
    gotoe = Goto('Goto_each',itr=var0)
    o1 = object_set()
    sc1 = Scan("Lamp", o1)
    i1 = Iterator()
    var1 = variable(i1.pretty_str(0))
    for1 = Foreach_obj(i1,o1)
    act1 = Act(var1,"Off","Lamp")
    for1.add_stmnt(act1)
    gotoe.add_stmnt(sc1)
    gotoe.add_stmnt(for1)
    program.add_stmnt(gotoe)
    return program



# execute the program on an environment
# prog = S5()
# env = E1()
# trace = prog.execute(env)
# demo = trace[2]
# print (prog.pretty_str())
# print (demo.pretty_str(1))