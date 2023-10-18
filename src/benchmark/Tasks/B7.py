import sys
sys.path.append('../..')
sys.path.append('../../Env')
from dsl import *

"""
Goto_each(li in L):
    O1 = Scan("Bottle")
    for each i1 in O1:
        action(i1,"Grab")
    O2 = Scan("Matchbox")
    for each i1 in O2:
        action(i1,"Grab")
        
Goto("Kitchen")
    O = Scan("Trash")
    let o = O[0]
    
    O3 = Scan("Bottle")
    for each i3 in O3:
        action(i3,"Place",["inside",o])
    O4 = Scan("Matchbox")
    for each i4 in O4:
        action(i4,"Place",["inside",o])
"""

#TODO: Get rid of nested gotos

def B7_prog():
    program = Prog(0)

    #First location
    itr0 = Iterator()
    gotoe = Goto('Goto_each',itr=itr0)
    os2 = object_set()
    os3 = object_set()
    sc2 = Scan("Bottle",os2)
    sc3 = Scan("Matchbox",os3)
    itr1 = Iterator()
    i1 = variable(itr1.pretty_str(0))
    for1 = Foreach_obj(itr1,os2)
    act1 = Act(i1,"Grab", "Bottle")

    for1.add_stmnt(act1)
    itr2 = Iterator()
    i2 = variable(itr2.pretty_str(0))
    for2 = Foreach_obj(itr2,os3)
    act1 = Act(i2,"Grab", "Matchbox")

    for2.add_stmnt(act1)
    gotoe.add_stmnt(sc2)
    gotoe.add_stmnt(for1)
    gotoe.add_stmnt(sc3)
    gotoe.add_stmnt(for2)

    #Last location
    var0 = variable("Kitchen_1")
    goto0 = Goto('Goto', loc=var0)
    os1 = object_set()
    sc1 = Scan("Trash",os1)
    var = variable("o")
    let1 = Let(var,os1,0, "Trash")

    os2 = object_set()
    os3 = object_set()
    sc2 = Scan("Bottle", os2)
    sc3 = Scan("Matchbox", os3)
    itr1 = Iterator()
    i1 = variable(itr1.pretty_str(0))
    for1 = Foreach_obj(itr1, os2)
    act2 = Act(i1,"Place", "Bottle", [["Inside", var]])

    for1.add_stmnt(act2)

    itr2 = Iterator()
    i2 = variable(itr2.pretty_str(0))
    for2 = Foreach_obj(itr2, os3)
    act2 = Act(i2,"Place", "Matchbox", [["Inside", var]])

    for2.add_stmnt(act2)

    goto0.add_stmnt(sc1)
    goto0.add_stmnt(let1)

    goto0.add_stmnt(sc2)
    goto0.add_stmnt(for1)
    goto0.add_stmnt(sc3)
    goto0.add_stmnt(for2)


    program.add_stmnt(gotoe)
    program.add_stmnt(goto0)
    return program

"""prog = B7_prog()
env = E1()
trace = prog.execute(env)
B7_demo_on_E1 = trace[2]
print(B7_demo_on_E1.pretty_str(1))"""