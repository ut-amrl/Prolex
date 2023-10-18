import sys
sys.path.append('../../..')
#sys.path.append('/Users/kiar-admin/Dev/Neurosymbolic-policies/')

from dsl import *
from benchmark.Environments.E1 import * 


"""
Survey Task 0 (go to the laundry room, collect the dry clothes, and put them into a basket)
GOTO(Laundry_room) 
    clothes = Scan("clothes")
    baskets = Scan("basket")
    let basket = baskets[0]
    foreach cloth in clothes:
        if (check_prop("dry",cloth)):
            action("grab",cloth)
            action(cloth,"place",basket,"in")
"""

def S0():
    program = Prog(0)
    # basket 
    basket_set = object_set()
    scan_baskets = Scan("Basket",basket_set)
    basket_var = variable("o1")
    let1 = Let(basket_var,basket_set,0, "Basket")
    
    # clothes
    clothe_set = object_set()
    scan_clothes = Scan("Clothes",clothe_set)
    cloth_iter = Iterator()
    i0  = variable(cloth_iter.pretty_str(0))
    for1 = Foreach_obj(cloth_iter,clothe_set)
    grab_clothe_act = Act(i0,"Grab", "Clothe")
    if_dry = If(Bexp('single', Check_prop(i0, "Dry", "Clothes")))
    place_in_basket_act = Act(i0, "Place", "Clothe", [["Inside", basket_var]])
    if_dry.add_stmnt(grab_clothe_act)   
    if_dry.add_stmnt(place_in_basket_act)
    for1.add_stmnt(if_dry)

    #
    var = variable('Washroom_1') # this can be changed to laundry room later
    goto1 = Goto('Goto', var)
    goto1.add_stmnt(scan_baskets)
    goto1.add_stmnt(let1)
    goto1.add_stmnt(scan_clothes)
    goto1.add_stmnt(for1)

    program.add_stmnt(goto1)
    return program



# # execute the program on an environment
# prog = S0()
# env = E1()
# print (env)
# trace = prog.execute(env)
# demo = trace[2]
# print (prog.pretty_str())
# print (demo.pretty_str(1))