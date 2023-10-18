import unittest
import random
from io import StringIO
import sys
from Env.objects import Object
from Env.relations import Relation

class relationsTests(unittest.TestCase):
    def test_single_relation_print(self):
        table = Object('Table', 1)
        cup = Object('Cup', 1)

        r1 = Relation('On', cup, table)

        #Check name implemented properly
        self.assertEqual('On_Cup_1_Table_1', r1.name)

        buffer = StringIO()
        sys.stdout = buffer

        r1.print()

        #Check that printing properly
        self.assertEqual(buffer.getvalue(), "Cup_1 is On Table_1\n")

    def test_multi_random_relation_print(self):
        cup = Object('Cup', 1)
        stove = Object('Stove', 1)

        rel_names = [
            'Beside',
            'Above',
            'Below',
            'Inside',
            'On'
        ]

        for i in range(1000):
            rand_rel_select = random.randint(0, 4)

            r = Relation(rel_names[rand_rel_select], cup, stove)

            # Check name implemented properly
            self.assertEqual(rel_names[rand_rel_select]+'_Cup_1_Stove_1', r.name)

            buffer = StringIO()
            sys.stdout = buffer

            r.print()

            # Check that printing properly
            self.assertEqual(buffer.getvalue(), "Cup_1 is "+ rel_names[rand_rel_select] + " Stove_1\n")


if __name__ == "__main__":
    unittest.main()