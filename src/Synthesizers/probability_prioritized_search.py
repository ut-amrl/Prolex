from dsl import *
from Synthesizers.find_hole import find_hole
from Synthesizers.ordered_hole_fills import ordered_hole_fills
from Synthesizers.fill_holes import fill_hole
from Synthesizers.check import *
import queue
import random

def probability_prioritized_search(sketch, demo, env):
    num_checked = 0
    Q = queue.PriorityQueue()
    Q.put((1, sketch))

    while not Q.empty():
        priority, popped_sketch = Q.get()

        #Get hole to fill
        hole_stmnt_pos, hole_idx = find_hole(popped_sketch)

        #Check if sketch is complete
        if hole_stmnt_pos == None:
            num_checked = num_checked + 1
            #Check if correct
            if check(demo, popped_sketch, deepcopy(env), printing=False): #Correct program
                return popped_sketch, num_checked

            continue

        # Get sorted order hole fills
        hole_fills_sorted = ordered_hole_fills(popped_sketch, env, hole_stmnt_pos, hole_idx, "GDFS_Test")

        #Loop through fills
        for fill in hole_fills_sorted:
            new_sketch = fill_hole(deepcopy(popped_sketch), hole_stmnt_pos, hole_idx, fill)
            assert new_sketch != None

            #TODO: Check infeasibility

            #TODO: Get Priority Value -- probably easiest to return this with the ordered hole fills

            #Push to Queue
            #Temp
            priority = random.randint(0, 100)
            Q.put((priority, new_sketch))

    return None, num_checked