import sys
sys.path.append('../../..')
#sys.path.append('/Users/kiar-admin/Dev/Neurosymbolic-policies/')


from dsl import *
from benchmark.Environments.E1 import * 


"""
Survey Task 1 (go to the kitchen; grab the towel; go to each room; clean all chairs)
goto(kitchen) 
    towels = Scan("Cleaning Tools")
    let towel = towels[0]
    action("grab",towel)
gotoeach_loc():
    chairs = Scan("Chair")
    foreach chair in chairs:
        action(chair,"clean")
"""

def S1():
    program = Prog(0)



    # go to washroom and grab a cleaning tool 
    washroom_var = variable('Washroom_1')
    goto_washroom = Goto('Goto', washroom_var)
    


    brush_set = object_set()
    brush_scan = Scan("Brush",brush_set)
    brush_var = variable(None)
    let_cleaning_tool = Let(brush_var,brush_set,0, "Brush")
    grab_brush_act = Act(brush_var, 'Grab')
    goto_washroom.add_stmnt(brush_scan)
    goto_washroom.add_stmnt(let_cleaning_tool)
    goto_washroom.add_stmnt(grab_brush_act)
    program.add_stmnt(goto_washroom)

    chair_set = object_set()
    scan_chairs = Scan("Chair",chair_set)
    chair_iter = Iterator()
    i0  = variable(chair_iter.pretty_str(0))
    for1 = Foreach_obj(chair_iter,chair_set)
    clean_chair_act = Act(i0,"Clean", "Chair")
    for1.add_stmnt(clean_chair_act)
    itr1 = Iterator()
    goto_each = Goto('Goto_each',itr=itr1)
    goto_each.add_stmnt(scan_chairs)
    goto_each.add_stmnt(for1)


    program.add_stmnt(goto_each)



    return program



# execute the program on an environment
# prog = S1()
# print(prog.pretty_str(0))
# env = E1()
# trace = prog.execute(env)
# demo = trace[2]
# print (prog.pretty_str())
# print (demo.pretty_str(1))