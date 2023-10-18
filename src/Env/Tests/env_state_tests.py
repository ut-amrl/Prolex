import unittest
import random
from Env.objects import Object
from Env.relations import Relation
from Env.locations import Location
from Env.robot import Robot
from Env.environment_state import Environment

class envTests(unittest.TestCase):
    def test_single_update_robot_loc(self):
        # Setup First Location
        table1 = Object('Table', 1)
        cup1 = Object('Cup', 1)

        r1 = Relation('On', cup1, table1)
        r2 = Relation('Below', table1, cup1)
        r3 = Relation('Above', cup1, table1)

        l1 = Location('Livingroom', 1,
                      {cup1.name: cup1, table1.name: table1},
                      {r1.name: r1, r2.name: r2, r3.name: r3})

        # Setup Second Location
        table2 = Object('Table', 2)
        cup2 = Object('Cup', 2)
        fan1 = Object('Fan', 1)

        r4 = Relation('On', cup2, table2)
        r5 = Relation('Below', table2, cup2)
        r6 = Relation('Above', cup2, table2)

        l2 = Location('Bedroom', 1,
                      {cup2.name: cup2, table2.name: table2, fan1.name: fan1},
                      {r4.name: r4, r5.name: r5, r6.name: r6})

        # Setup Robot
        robot = Robot()

        # Make env
        env = Environment({l1.name: l1, l2.name: l2}, robot, l1.name)

        # Test Location update
        env.update_robot_loc(l2.name)

        self.assertEqual(env.robot_loc, l2.name)

    def test_multi_rand_update_robot_loc(self):
        # Setup First Location
        table1 = Object('Table', 1)
        cup1 = Object('Cup', 1)

        r1 = Relation('On', cup1, table1)
        r2 = Relation('Below', table1, cup1)
        r3 = Relation('Above', cup1, table1)

        l1 = Location('Livingroom', 1,
                      {cup1.name: cup1, table1.name: table1},
                      {r1.name: r1, r2.name: r2, r3.name: r3})

        # Setup Second Location
        table2 = Object('Table', 2)
        cup2 = Object('Cup', 2)
        fan1 = Object('Fan', 1)

        r4 = Relation('On', cup2, table2)
        r5 = Relation('Below', table2, cup2)
        r6 = Relation('Above', cup2, table2)

        l2 = Location('Bedroom', 1,
                      {cup2.name: cup2, table2.name: table2, fan1.name: fan1},
                      {r4.name: r4, r5.name: r5, r6.name: r6})

        #Make empty locations
        l3 = Location('Bedroom', 2, {}, {})
        l4 = Location('Kitchen', 1, {}, {})
        l5 = Location('Washroom', 1, {}, {})

        # Setup Robot
        robot = Robot()

        # Make env
        locations = {
            l1.name: l1,
            l2.name: l2,
            l3.name: l3,
            l4.name: l4,
            l5.name: l5
        }

        location_names = [
            l1.name,
            l2.name,
            l3.name,
            l4.name,
            l5.name
        ]

        env = Environment(locations, robot, l1.name)

        for i in range(1000):
            new_loc_select = random.randint(0, 4)

            new_loc_name = location_names[new_loc_select]

            #Update robot location
            env.update_robot_loc(new_loc_name)

            #Check
            self.assertEqual(env.robot_loc, new_loc_name)


if __name__ == "__main__":
    unittest.main()