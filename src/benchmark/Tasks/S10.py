import sys
sys.path.append('../../..')

from dsl import *
from benchmark.Environments.E1 import * 


"""
Survey Task 10 (go to the kitchen; grab all vegetables and fruits that are spoilt; put them in the garbage bin)
Goto('Kitchen_1'):
    O2 = Scan('Trash')
    let o2 = O2[0]
    O3 = Scan('Vegetable')
    for i0 in O3:
        if Check_prop(i0, 'Spoilt'):
            act(i0, 'Grab')
            act(i0,'Place',[['Inside',o2]])
    O4 = Scan('Fruit')
    for i1 in O4:
        if Check_prop(i1, 'Spoilt'):
            act(i1, 'Grab')
            act(i1,'Place',[['Inside',o2]])
"""

def S10():
    program = Prog(0)
    var0 = variable('Kitchen_1')
    goto = Goto('Goto',loc=var0)
    os2 = object_set()
    sc2 = Scan('Trash',os2)
    var2 = variable("o2")
    let2 = Let(var2,os2,0)
    os3 = object_set()
    sc3 = Scan('Vegetable',os3)
    itr0 = Iterator()
    var3 = variable(itr0.pretty_str(0))
    for1 = Foreach_obj(itr0,os3)
    if1 = If(Bexp('single',Check_prop(var3,'Spoil', 'Vegetable')))
    act2 = Act(var3,'Grab', 'Vegetable')
    act3 = Act(var3,'Place', 'Vegetable',[['Inside',var2]])
    os4 = object_set()
    sc4 = Scan('Fruit',os4)
    itr1 = Iterator()
    var4 = variable(itr1.pretty_str(0))
    for2 = Foreach_obj(itr1,os4)
    if2 = If(Bexp('single',Check_prop(var4,'Spoil', 'Fruit')))
    act4 = Act(var4,'Grab', 'Fruit')
    act5 = Act(var4,'Place', 'Fruit',[['Inside',var2]])
    if1.add_stmnt(act2)
    if1.add_stmnt(act3)
    for1.add_stmnt(if1)
    if2.add_stmnt(act4)
    if2.add_stmnt(act5)
    for2.add_stmnt(if2)
    goto.add_stmnt(sc2)
    goto.add_stmnt(let2)
    goto.add_stmnt(sc3)
    goto.add_stmnt(for1)
    goto.add_stmnt(sc4)
    goto.add_stmnt(for2)
    program.add_stmnt(goto)
    return program



# execute the program on an environment
# prog = S10()
# env = E1()
# trace = prog.execute(env)
# demo = trace[2]
# print (prog.pretty_str())
# print (demo.pretty_str(1))
