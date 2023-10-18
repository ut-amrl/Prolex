import unittest
import random
from Env.objects import Object
from Env import env_def

class objectTests(unittest.TestCase):
    def test_single_update_state(self):
        fan = Object('Fan', 1)
        cup = Object('Cup', 1)

        cup.update_state('Full', True)
        fan.update_state('On', True)

        self.assertTrue(cup.props['Full'])
        self.assertTrue(fan.props['On'])

    def test_multi_random_update_state(self):
        fan = Object('Fan', 1)
        stove = Object('Stove', 1)
        cup = Object('Cup', 1)

        obj_dict = {
            fan.name: fan,
            stove.name: stove,
            cup.name: cup
        }

        obj_names = [
            fan.name,
            stove.name,
            cup.name
        ]

        for i in range(1000):
            rand_obj_select = random.randint(0, 2)
            rand_bool_select = random.randint(0, 1)

            if rand_bool_select == 0:
                obj = obj_dict[obj_names[rand_obj_select]]
                obj.update_state(env_def.properties[obj.tp][0], False)

                self.assertFalse(obj.props[env_def.properties[obj.tp][0]])

            else:
                obj = obj_dict[obj_names[rand_obj_select]]
                obj.update_state(env_def.properties[obj.tp][0], True)

                self.assertTrue(obj.props[env_def.properties[obj.tp][0]])

if __name__ == "__main__":
    unittest.main()