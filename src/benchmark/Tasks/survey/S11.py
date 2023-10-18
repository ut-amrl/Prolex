import sys
sys.path.append('../../..')

from dsl import *
from benchmark.Environments.E1 import * 


"""
Survey Task 11 (Go to all rooms, open all windows, get the cleaning tools from the living room, sweep the floors, close all windows)
Goto('Livingroom'):
    O1 = Scan('Cleaning Tools')
    let o1 = O1[0]
Goto_each():
    O2 = Scan('Window')
    let o2 = O2[0]
    act(o2,"Open")
    O3 = Scan('Floor')
    let o3 = O3[0]
    act(o3,'Clean')
    act(o2,"Close")
    """

def S11():
    program = Prog(0)
    var0 = variable('Livingroom_1')
    goto = Goto('Goto',loc=var0)
    os1 = object_set()
    sc1 = Scan('Cleaning',os1)
    var1 = variable("o1")
    let1 = Let(var1,os1,0)
    grab_tools = Act(var1, 'Grab', "Cleaning")
    itr0 = Iterator()
    gotoe = Goto('Goto_each',itr=itr0)
    os2 = object_set()
    sc2 = Scan('Window',os2)
    var2 = variable("o2")
    let2 = Let(var2,os2,0)
    act1 = Act(var2,"Open", "Window")
    os3 = object_set()
    sc3 = Scan('Floor',os3)
    var3 = variable("o3")
    let3 = Let(var3,os3,0)
    act2 = Act(var3,'Clean', 'Floor')
    act3 = Act(var2,'Close', 'Window')
    gotoe.add_stmnt(sc2)
    gotoe.add_stmnt(let2)
    gotoe.add_stmnt(act1)
    gotoe.add_stmnt(sc3)
    gotoe.add_stmnt(let3)
    gotoe.add_stmnt(act2)
    gotoe.add_stmnt(act3)
    goto.add_stmnt(sc1)
    goto.add_stmnt(let1)
    goto.add_stmnt(grab_tools)
    program.add_stmnt(goto)
    program.add_stmnt(gotoe)
    return program



# execute the program on an environment
# prog = S11()
# print(prog.pretty_str(0))
# env = E1()
# trace = prog.execute(env)
# demo = trace[2]
# print (prog.pretty_str())
# print (demo.pretty_str(1))