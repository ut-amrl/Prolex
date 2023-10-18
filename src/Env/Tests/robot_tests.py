import unittest
import random
from Env.objects import Object
from Env.robot import Robot

class robotTests(unittest.TestCase):
    def test_single_add_object(self):
        table = Object('Table', 1)

        r = Robot()
        r.add_object(table)

        self.assertEqual(r.objects[table.name], table)

    def test_single_add_remove_object(self):
        table = Object('Table', 1)

        r = Robot()
        r.add_object(table)

        self.assertEqual(r.objects[table.name], table)

        r.remove_object(table.name)

        self.assertEqual(len(r.objects), 0)

    def test_multi_random_add_remove_object(self):
        added_objects = []
        r = Robot()
        num_added_objects = 0
        for i in range(1000):
            add_remove_select = random.randint(0, 1)

            if add_remove_select == 0 and len(r.objects) > 0: #Remove object case
                #Pick object to remove
                obj_remove_sel = random.randint(0, len(added_objects) - 1)
                obj_to_remove = added_objects[obj_remove_sel]

                current_dict = r.objects.copy()
                current_dict.pop(obj_to_remove.name)

                removed_obj = r.remove_object(obj_to_remove.name)

                self.assertEqual(removed_obj.name, obj_to_remove.name)
                self.assertDictEqual(r.objects, current_dict)

                added_objects.pop(obj_remove_sel)

            else:
                num_added_objects = num_added_objects + 1
                new_fan = Object('Fan', num_added_objects)

                current_dict = r.objects.copy()
                current_dict[new_fan.name] = new_fan

                r.add_object(new_fan)
                added_objects.append(new_fan)

                self.assertDictEqual(r.objects, current_dict)


if __name__ == "__main__":
    unittest.main()