import sys
sys.path.append('../../..')

from dsl import *
from benchmark.Environments.E1 import * 


"""
Survey Task 14 (go to bedroom, open the cupboard, pickup the pillow, put it on the bed)
Goto_each():
    O1 = Scan('Cupboard')
    let o1 = O1[0]
    act(o1,'Open')
    O2 = Scan('Pillow')
    let o2 = O2[0]
    act(o2,"Grab")
    O3 = Scan('Bed')
    let o3 = O3[0]
    act(o2,"Place",[["On",o3]])
"""

def S14_prog():
    program = Prog(0)
    itr0 = variable('Bedroom_1')
    gotoe = Goto('Goto',loc=itr0)
    os1 = object_set()
    sc1 = Scan('Cupboard',os1)
    var1 = variable("o1")
    let1 = Let(var1,os1,0)
    act1 = Act(var1,'Open','Cupboard')
    os2 = object_set()
    sc2 = Scan('Pillow',os2)
    var2 = variable("o2")
    let2 = Let(var2,os2,0)
    act2 = Act(var2,'Grab','Pillow')
    os3 = object_set()
    sc3 = Scan('Bed',os3)
    var3 = variable("o3")
    let3 = Let(var3,os3,0)
    act3 = Act(var2,'Place','Pillow',[['On',var3]])
    gotoe.add_stmnt(sc1)
    gotoe.add_stmnt(let1)
    gotoe.add_stmnt(act1)
    gotoe.add_stmnt(sc2)
    gotoe.add_stmnt(let2)
    gotoe.add_stmnt(act2)
    gotoe.add_stmnt(sc3)
    gotoe.add_stmnt(let3)
    gotoe.add_stmnt(act3)
    program.add_stmnt(gotoe)
    return program



# execute the program on an environment
# prog = S14()
# env = E1()
# trace = prog.execute(env)
# demo = trace[2]
# print (prog.pretty_str())
# print (demo.pretty_str(1))