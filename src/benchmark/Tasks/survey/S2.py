import sys
sys.path.append('../../..')
#sys.path.append('/Users/kiar-admin/Dev/Neurosymbolic-policies/')
from benchmark.Environments.E1 import *
from dsl import *

"""
Survey Task 2 (go to the Livingroom_1; 
               grab all clothes; 
               find a basket and put the clothes in it; 
               bring the basket to the Bedroom_3)
"""


def S2():
    program = Prog(0)
    # go to Livingroom_1
    lr1_var = variable('Livingroom_1')
    goto_lr1 = Goto('Goto', lr1_var)

    # basket
    basket_set = object_set()
    scan_baskets = Scan("Basket", basket_set)
    basket_var = variable("basket_var")
    let1 = Let(basket_var, basket_set, 0, "Basket")
    goto_lr1.add_stmnt(scan_baskets)
    goto_lr1.add_stmnt(let1)
    # clothes
    clothe_set = object_set()
    scan_clothes = Scan("Clothes", clothe_set)
    cloth_iter = Iterator()
    i0 = variable(cloth_iter.pretty_str(0))
    for1 = Foreach_obj(cloth_iter, clothe_set)
    grab_clothe_act = Act(i0, "Grab", "Clothe")
    place_in_basket_act = Act(i0, "Place", "Clothe", [["Inside", basket_var]])
    for1.add_stmnt(grab_clothe_act)
    for1.add_stmnt(place_in_basket_act)
    goto_lr1.add_stmnt(scan_clothes)
    goto_lr1.add_stmnt(for1)

    grab_basket_act = Act(basket_var, "Grab", "Basket")
    goto_lr1.add_stmnt(grab_basket_act)
    program.add_stmnt(goto_lr1)

    # go to Bedroom_3
    br1_var = variable('Bedroom_1')
    goto_br1 = Goto('Goto', br1_var)

    basket_set2 = object_set()
    scan_baskets2 = Scan("Basket", basket_set2)
    basket_var2 = variable(None)
    let2 = Let(basket_var2, basket_set2, 0, "Basket")

    floor_set = object_set()
    scan_floor = Scan("Floor", floor_set)
    floor_var = variable(None)
    let_floor = Let(floor_var, floor_set, 0, 'Floor')

    place_basket = Act(basket_var, 'Place', 'Basket',  [["On", floor_var]])

    goto_br1.add_stmnt(scan_baskets2)
    goto_br1.add_stmnt(let2)
    goto_br1.add_stmnt(scan_floor)
    goto_br1.add_stmnt(let_floor)
    goto_br1.add_stmnt(place_basket)


    program.add_stmnt(goto_br1)
    return program


# # execute the program on an environment
# prog = S2()
# print(prog.pretty_str(0, debug=True))
# env = E1()
# trace = prog.execute(env)
# demo = trace[2]
# print(prog.pretty_str())
# print(demo.pretty_str(1))
