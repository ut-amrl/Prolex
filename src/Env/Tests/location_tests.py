import unittest
import random
import copy
from Env import env_def
from Env.objects import Object
from Env.relations import Relation
from Env.locations import Location

class locTests(unittest.TestCase):
    def test_relation_fetching(self):
        table = Object('Table', 1)
        stove = Object('Stove', 1)
        cup1 = Object('Cup', 1)
        cup2 = Object('Cup', 2)

        r1 = Relation('On', cup1, table)
        r2 = Relation('Below', table, cup1)
        r3 = Relation('Above', cup1, table)
        r4 = Relation('Inside', cup2, stove)

        objects = {
            table.name: table,
            stove.name: stove,
            cup1.name: cup1,
            cup2.name: cup2
        }

        relations = {
            r1.name: r1,
            r2.name: r2,
            r3.name: r3,
            r4.name: r4
        }

        location = Location('Livingroom', 1,
                      objects, relations)

        #Get Cup_1 Relations
        found_rels = location.get_relations(cup1.name)
        sub_relations = [r1, r2, r3]

        for i in range(len(found_rels)):
            self.assertEqual(found_rels[i].name, sub_relations[i].name)

        #Get Table_1 relations
        found_rels = location.get_relations(table.name)

        for i in range(len(found_rels)):
            self.assertEqual(found_rels[i].name, sub_relations[i].name)

        #Get Cup_1 x Table_1 relations
        found_rels = location.get_relations(cup1.name, table.name)

        for i in range(len(found_rels)):
            self.assertEqual(found_rels[i].name, sub_relations[i].name)

        found_rels = location.get_relations(table.name, cup1.name)

        for i in range(len(found_rels)):
            self.assertEqual(found_rels[i].name, sub_relations[i].name)

        #Get Cup_2 relations
        found_rels = location.get_relations(cup2.name)
        sub_relations = [r4]

        for i in range(len(found_rels)):
            self.assertEqual(found_rels[i].name, sub_relations[i].name)

        # Get Stove_1 relations
        found_rels = location.get_relations(stove.name)

        for i in range(len(found_rels)):
            self.assertEqual(found_rels[i].name, sub_relations[i].name)

        #Get Cup_2 x Stove_1 relations
        found_rels = location.get_relations(cup2.name, stove.name)

        for i in range(len(found_rels)):
            self.assertEqual(found_rels[i].name, sub_relations[i].name)

        found_rels = location.get_relations(stove.name, cup2.name)

        for i in range(len(found_rels)):
            self.assertEqual(found_rels[i].name, sub_relations[i].name)

        #Get Cup_1 x Stove_1 relations (should be empty)
        found_rels = location.get_relations(cup1.name, stove.name)
        self.assertEqual(len(found_rels), 0)
        found_rels = location.get_relations(stove.name, cup1.name)
        self.assertEqual(len(found_rels), 0)

        # Get Cup_2 x Table_1 relations (should be empty)
        found_rels = location.get_relations(cup2.name, table.name)
        self.assertEqual(len(found_rels), 0)
        found_rels = location.get_relations(table.name, cup2.name)
        self.assertEqual(len(found_rels), 0)

    def test_single_add_object(self):
        table = Object('Table', 1)
        stove = Object('Stove', 1)
        cup1 = Object('Cup', 1)
        cup2 = Object('Cup', 2)

        r1 = Relation('On', cup1, table)
        r2 = Relation('Below', table, cup1)
        r3 = Relation('Above', cup1, table)
        r4 = Relation('Inside', cup2, stove)

        objects = {
            table.name: table,
            stove.name: stove,
            cup1.name: cup1,
            cup2.name: cup2
        }

        relations = {
            r1.name: r1,
            r2.name: r2,
            r3.name: r3,
            r4.name: r4
        }

        location = Location('Livingroom', 1,
                            objects, relations)

        new_obj = Object('Fan', 1)
        current_obj = location.objects.copy()
        current_obj[new_obj.name] = new_obj

        current_rel = location.relations.copy()

        location.add_object(new_obj)

        self.assertDictEqual(current_obj, location.objects)
        self.assertDictEqual(current_rel, location.relations)

    def test_single_remove_obj(self):
        table = Object('Table', 1)
        stove = Object('Stove', 1)
        cup1 = Object('Cup', 1)
        cup2 = Object('Cup', 2)

        r1 = Relation('On', cup1, table)
        r2 = Relation('Below', table, cup1)
        r3 = Relation('Above', cup1, table)
        r4 = Relation('Inside', cup2, stove)

        objects = {
            table.name: table,
            stove.name: stove,
            cup1.name: cup1,
            cup2.name: cup2
        }

        relations = {
            r1.name: r1,
            r2.name: r2,
            r3.name: r3,
            r4.name: r4
        }

        location = Location('Livingroom', 1,
                            objects, relations)

        for i in range(4):
            loc_copy = copy.deepcopy(location)
            if i == 0:
                current_obj = loc_copy.objects.copy()
                current_obj.pop('Table_1')
                current_rel = {
                    r4.name: r4
                }

                loc_copy.remove_object('Table_1')

                for obj in current_obj:
                    actual_obj = loc_copy.objects[obj]
                    self.assertEqual(obj, actual_obj.name)

                    for prop in env_def.properties[current_obj[obj].tp]:
                        self.assertEqual(current_obj[obj].props[prop], actual_obj.props[prop])

                for rel in current_rel:
                    actual_rel = loc_copy.relations[rel]
                    self.assertEqual(rel, actual_rel.name)

            elif i == 1:
                current_obj = loc_copy.objects.copy()
                current_obj.pop('Stove_1')
                current_rel = {
                    r1.name: r1,
                    r2.name: r2,
                    r3.name: r3
                }

                loc_copy.remove_object('Stove_1')

                for obj in current_obj:
                    actual_obj = loc_copy.objects[obj]
                    self.assertEqual(obj, actual_obj.name)

                    for prop in env_def.properties[current_obj[obj].tp]:
                        self.assertEqual(current_obj[obj].props[prop], actual_obj.props[prop])

                for rel in current_rel:
                    actual_rel = loc_copy.relations[rel]
                    self.assertEqual(rel, actual_rel.name)

            elif i == 2:
                current_obj = loc_copy.objects.copy()
                current_obj.pop('Cup_1')
                current_rel = {
                    r4.name: r4
                }

                loc_copy.remove_object('Cup_1')

                for obj in current_obj:
                    actual_obj = loc_copy.objects[obj]
                    self.assertEqual(obj, actual_obj.name)

                    for prop in env_def.properties[current_obj[obj].tp]:
                        self.assertEqual(current_obj[obj].props[prop], actual_obj.props[prop])

                for rel in current_rel:
                    actual_rel = loc_copy.relations[rel]
                    self.assertEqual(rel, actual_rel.name)

            else:
                current_obj = loc_copy.objects.copy()
                current_obj.pop('Cup_2')
                current_rel = {
                    r1.name: r1,
                    r2.name: r2,
                    r3.name: r3
                }

                loc_copy.remove_object('Cup_2')

                for obj in current_obj:
                    actual_obj = loc_copy.objects[obj]
                    self.assertEqual(obj, actual_obj.name)

                    for prop in env_def.properties[current_obj[obj].tp]:
                        self.assertEqual(current_obj[obj].props[prop], actual_obj.props[prop])

                for rel in current_rel:
                    actual_rel = loc_copy.relations[rel]
                    self.assertEqual(rel, actual_rel.name)

    def test_single_add_rel(self):
        table = Object('Table', 1)
        stove = Object('Stove', 1)
        cup1 = Object('Cup', 1)
        cup2 = Object('Cup', 2)

        r1 = Relation('On', cup1, table)
        r2 = Relation('Below', table, cup1)
        r3 = Relation('Above', cup1, table)
        r4 = Relation('Inside', cup2, stove)

        objects = {
            table.name: table,
            stove.name: stove,
            cup1.name: cup1,
            cup2.name: cup2
        }

        relations = {
            r1.name: r1,
            r2.name: r2,
            r3.name: r3,
            r4.name: r4
        }

        location = Location('Livingroom', 1,
                            objects, relations)

        new_rel = Relation('Beside', table, stove)
        current_obj = location.objects.copy()
        current_rel = location.relations.copy()
        current_rel[new_rel.name] = new_rel

        location.add_relation(new_rel)

        self.assertDictEqual(current_obj, location.objects)
        self.assertDictEqual(current_rel, location.relations)

    def test_single_remove_rel(self):
        table = Object('Table', 1)
        stove = Object('Stove', 1)
        cup1 = Object('Cup', 1)
        cup2 = Object('Cup', 2)

        r1 = Relation('On', cup1, table)
        r2 = Relation('Below', table, cup1)
        r3 = Relation('Above', cup1, table)
        r4 = Relation('Inside', cup2, stove)

        objects = {
            table.name: table,
            stove.name: stove,
            cup1.name: cup1,
            cup2.name: cup2
        }

        relations = {
            r1.name: r1,
            r2.name: r2,
            r3.name: r3,
            r4.name: r4
        }

        location = Location('Livingroom', 1,
                            objects, relations)

        for i in range(4):
            loc_copy = copy.deepcopy(location)
            if i == 0:
                current_obj = loc_copy.objects.copy()
                current_rel = loc_copy.relations.copy()
                current_rel.pop(r1.name)

                loc_copy.remove_relation(r1.name)

                for obj in current_obj:
                    actual_obj = loc_copy.objects[obj]
                    self.assertEqual(obj, actual_obj.name)

                    for prop in env_def.properties[current_obj[obj].tp]:
                        self.assertEqual(current_obj[obj].props[prop], actual_obj.props[prop])

                for rel in current_rel:
                    actual_rel = loc_copy.relations[rel]
                    self.assertEqual(rel, actual_rel.name)

            elif i == 1:
                current_obj = loc_copy.objects.copy()
                current_rel = loc_copy.relations.copy()
                current_rel.pop(r2.name)

                loc_copy.remove_relation(r2.name)

                for obj in current_obj:
                    actual_obj = loc_copy.objects[obj]
                    self.assertEqual(obj, actual_obj.name)

                    for prop in env_def.properties[current_obj[obj].tp]:
                        self.assertEqual(current_obj[obj].props[prop], actual_obj.props[prop])

                for rel in current_rel:
                    actual_rel = loc_copy.relations[rel]
                    self.assertEqual(rel, actual_rel.name)

            elif i == 2:
                current_obj = loc_copy.objects.copy()
                current_rel = loc_copy.relations.copy()
                current_rel.pop(r3.name)

                loc_copy.remove_relation(r3.name)

                for obj in current_obj:
                    actual_obj = loc_copy.objects[obj]
                    self.assertEqual(obj, actual_obj.name)

                    for prop in env_def.properties[current_obj[obj].tp]:
                        self.assertEqual(current_obj[obj].props[prop], actual_obj.props[prop])

                for rel in current_rel:
                    actual_rel = loc_copy.relations[rel]
                    self.assertEqual(rel, actual_rel.name)

            else:
                current_obj = loc_copy.objects.copy()
                current_rel = loc_copy.relations.copy()
                current_rel.pop(r4.name)

                loc_copy.remove_relation(r4.name)

                for obj in current_obj:
                    actual_obj = loc_copy.objects[obj]
                    self.assertEqual(obj, actual_obj.name)

                    for prop in env_def.properties[current_obj[obj].tp]:
                        self.assertEqual(current_obj[obj].props[prop], actual_obj.props[prop])

                for rel in current_rel:
                    actual_rel = loc_copy.relations[rel]
                    self.assertEqual(rel, actual_rel.name)

if __name__ == "__main__":
    unittest.main()