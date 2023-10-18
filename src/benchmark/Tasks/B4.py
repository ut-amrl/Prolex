import sys
sys.path.append('../..')
sys.path.append('../../Env')
from dsl import *

"""
Bringing in wood
Goto_each(i0):
    O1 = Scan("wood")
    for each i1 in O1:
        action(i1,"pick")
        
Goto('kitchen)
    O1 = Scan("fridge")
    let o1 = O1[0]
    O2 = Scan("wood")
    for each i1 in O2:
        action(i1,"place",o1,"near")
"""

def B4_prog():
    program = Prog(0)

    #GOTO EACH
    itr0 = Iterator()
    var2 = variable(itr0.pretty_str(0))
    gotoe = Goto('Goto_each', itr=var2)
    os2 = object_set()
    sc2 = Scan("Wood", os2)
    itr1 = Iterator()
    i0  = variable(itr1.pretty_str(0))
    for1 = Foreach_obj(itr1,os2)
    act1 = Act(i0,"Grab","Wood")
    for1.add_stmnt(act1)
    gotoe.add_stmnt(sc2)
    gotoe.add_stmnt(for1)

    #GOTO KITCHEN
    var0 = variable('Kitchen_1')
    goto1 = Goto('Goto', loc=var0)
    os1 = object_set()
    sc1 = Scan("Fridge",os1)
    var1 = variable("o1")
    let1 = Let(var1,os1,0)

    os3 = object_set()
    sc3 = Scan("Wood", os3)
    itr2 = Iterator()
    for2 = Foreach_obj(itr2, os3)
    act2 = Act(itr2, "Place", "Wood", [["Near", var1]])
    for2.add_stmnt(act2)

    goto1.add_stmnt(sc1)
    goto1.add_stmnt(let1)
    goto1.add_stmnt(sc3)
    goto1.add_stmnt(for2)


    program.add_stmnt(gotoe)
    program.add_stmnt(goto1)
    return program

# prog = B4_prog()
#
# print(prog.pretty_str(0))
# env = E2()
# trace = prog.execute(env)
# B4_demo_on_E2 = trace[2]
# print(B4_demo_on_E2.pretty_str(1))