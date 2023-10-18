import sys
sys.path.append('../..')
sys.path.append('../../Env')
from dsl import *

"""
Cleaning up after a meal
O = Scan("table")
let o = O[0]
O1 = Scan("cup")
O2 = Scan("plate")
O3 = Scan("chair")
for i1 in O1:
    if check_rel(i1,o,"on"):
        action(i1,"clean")
for i2 in O2:
    if check_rel(i2,o,"on"):
        action(i2,"clean")
for i3 in O3:
    if check_rel(i3,o,"near"):
        action(i3,"clean")
"""

def B8_prog():
    program = Prog(0)
    os1 = object_set()
    sc1 = Scan("Table",os1)
    var0 = variable("o")
    let1 = Let(var0,os1,0, "Table")
    os2 = object_set()
    sc2 = Scan("Cup", os2)
    os3 = object_set()
    sc3 = Scan("Plate", os3)
    os4 = object_set()
    sc4 = Scan("Chair", os4)
    itr1 = Iterator()
    var1 = variable(itr1.pretty_str(0))
    for1 = Foreach_obj(itr1,os2)
    if1 = If(Bexp('single',Check_rel(var1,var0,"On", "Cup", "Table")))
    act1 = Act(var1,"Clean", "Cup")
    if1.add_stmnt(act1)
    for1.add_stmnt(if1)
    itr2 = Iterator()
    var2 = variable(itr2.pretty_str(0))
    for2 = Foreach_obj(itr2,os3)
    if2 = If(Bexp('single',Check_rel(var2,var0,"On", "Plate", "Table")))
    act2 = Act(var2,"Clean", "Plate")
    if2.add_stmnt(act2)
    for2.add_stmnt(if2)
    itr3 = Iterator()
    var3 = variable(itr3.pretty_str(0))
    for3 = Foreach_obj(itr3,os4)
    if3 = If(Bexp('single',Check_rel(var3,var0,"Near", "Chair", "Table")))
    act3 = Act(var3,"Clean", "Chair")
    if3.add_stmnt(act3)
    for3.add_stmnt(if3)
    var = variable("Kitchen_1")
    goto1 = Goto("Goto", var)

    goto1.add_stmnt(sc1)
    goto1.add_stmnt(let1)
    goto1.add_stmnt(sc2)
    goto1.add_stmnt(sc3)
    goto1.add_stmnt(sc4)
    goto1.add_stmnt(for1)
    goto1.add_stmnt(for2)
    goto1.add_stmnt(for3)

    program.add_stmnt(goto1)

    return program
# prog = B8_prog()
# env = E1()
# trace = prog.execute(env)
# B8_demo_on_E1 = trace[2]
# print(B8_demo_on_E1.pretty_str(1))