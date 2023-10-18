import sys
sys.path.append('../..')
sys.path.append('../../Env')
from Env.objects import Object
from Env.relations import Relation
from Env.locations import Location
from Env.robot import Robot
from Env.environment_state import Environment
def E():
    objs = [Object('Drawer', 0), Object('Drawer',1),Object('Book',1,['Red']),Object('Book',2,['White']),Object('Book',3,['Green']),Object('Cupboard',1),
    Object('Box',1),Object('Pen',1),Object('Plate',1),Object('Wood',1),Object('Door',1,['Open']),Object('Trash',1),Object('Bottle',1),Object('Bottle',2), Object('Bottle',3),
    Object('Matchbox',1), Object('Matchbox',2), Object('Matchbox',3),Object('Table',1),Object('Spoon',1),Object('Fork',1),Object('Chair',1),Object('Cup',1),Object('Floor',1),
    Object('Cleaning',1),Object('Window',1),Object('Plant',1),Object('Basket',1),Object('Clothes',1),Object('Drawer',2), Object('Lamp', 6), Object('Lamp', 7), Object('Book', 4, ['Red']), Object('Box', 4), Object('Door', 2)]
    rels = [Relation('Above',objs[20],objs[13]), Relation('Near', objs[33], objs[10])]
    dict1 = {}
    for obj in objs:
        dict1[obj.name] = obj
    dict2 = {}
    for rel in rels:
        dict2[rel.name] = rel
    l1 = Location('Livingroom',1,dict1,dict2)
    objs = [Object('Wood',2), Object('Wood',3), Object('Brush',1), Object('Clothes',2), Object('Clothes',3), Object('Clothes',4),Object('Bed',1),Object('Drawer',3),Object('Door',3,['Open','Blue']), Object('Door',4,['Open','Blue']),Object('Bottle',4),
    Object('Box',2),Object('Table',2),Object('Lamp',1),Object('Floor',2),Object('Window',2,['Open']),Object('Plate',2,['Hot','Full']),Object('Cup',2,['Broken']),
    Object('Book',5,['Green']),Object('Book',6,['Red']),Object('Lamp',1,['On']),Object('Light',1,['On']),Object('Chair',2),
    Object('Pillow',1),Object('Cupboard',2),Object('Pillow',2), Object('Matchbox',4), Object('Bottle',5), Object('Bottle',6), Object('Lamp', 2), Object('Lamp', 3), Object('Lamp', 4), Object('Lamp', 5)]
    rels = [Relation('Near',objs[6],objs[7]),Relation('Near',objs[8],objs[4]),Relation('Near',objs[6],objs[4]),Relation('On',objs[13],objs[7]),
    Relation('On',objs[14],objs[7]),Relation('Beside',objs[15],objs[7]),Relation('Above',objs[16],objs[7]),Relation('Near',objs[10],objs[7]),
    Relation('Above',objs[10],objs[7]),Relation('On',objs[18],objs[2]),Relation('On',objs[13],objs[2]),Relation('Inside',objs[20],objs[19]),
            Relation('Near', objs[29], objs[8]), Relation('Near', objs[30], objs[8]), Relation('Near', objs[31], objs[8]), Relation('Near', objs[32], objs[8]),
            Relation('On', objs[23], objs[6]), Relation('On', objs[18], objs[6]), Relation('On', objs[19], objs[6])]
    dict1 = {}
    for obj in objs:
        dict1[obj.name] = obj
    dict2 = {}
    for rel in rels:
        dict2[rel.name] = rel
    l2 = Location('Bedroom',1,dict1,dict2)
    objs = [Object('Counter',1),Object('Fridge',1),Object('Fruit',1),Object('Fruit',2),Object('Table',3),Object('Vegetable',1),
    Object('Sink',1),Object('Plate',3),Object('Door',5,['Open']),Object('Bottle',7),Object('Matchbox',5),Object('Drawer',4),
    Object('Cereal',1),Object('Cupboard',3),Object('Fruit',3),Object('Vegetable',2),Object('Floor',3),Object('Window',3),
    Object('Stove',1),Object('Pot',1),Object('Pan',1),Object('Dishwasher',1),Object('Plate',4),Object('Cup',3),Object('Chair',3),
    Object('Cleaning',2),Object('Mug',1),Object('Trash',2),Object('Stove',2, ['On']), Object('Cup',4), Object('Cup',5), Object('Cup',6),
            Object('Plate',5), Object('Plate',6), Object('Plate',7), Object('Chair',4), Object('Chair',5), Object('Chair',6),Object('Matchbox',6), Object('Bottle',8), Object('Wood',4),
            Object('Lamp', 8), Object('Book', 7, ['Red']), Object('Book', 8, ['Red']), Object('Book', 9, ['Red']), Object('Plate', 8), Object('Mug', 2),
            Object('Vegetable', 9, ['Spoil']), Object('Vegetable', 10, ['Spoil']), Object('Fruit', 9, ['Spoil']), Object('Fruit', 10, ['Spoil'])]
    rels = [Relation('Inside',objs[2],objs[1]),Relation('Inside',objs[3],objs[1]),Relation('Inside',objs[5],objs[1]),
    Relation('Inside',objs[22],objs[21]),Relation('Inside',objs[23],objs[21]), Relation('Inside',objs[26],objs[21]),
            Relation('On', objs[29], objs[4]), Relation('On', objs[30], objs[4]), Relation('On', objs[31], objs[4]),
            Relation('On', objs[32], objs[4]), Relation('On', objs[33], objs[4]), Relation('On', objs[34], objs[4]),
            Relation('Near', objs[35], objs[4]), Relation('Near', objs[36], objs[4]), Relation('Near', objs[37], objs[4]),
            Relation('Inside', objs[45], objs[21]), Relation('Inside', objs[46], objs[21])
            ]
    dict1 = {}
    for obj in objs:
        dict1[obj.name] = obj
    dict2 = {}
    for rel in rels:
        dict2[rel.name] = rel
    l3 = Location('Kitchen',1,dict1,dict2)
    objs = [Object('Matchbox',7), Object('Matchbox',8),Object('Bottle',9), Object('Wood',5), Object('Door',6,['Open']), Object('Floor',4),Object('Window',4),Object('Basket',2),
    Object('Clothes',5),Object('Clothes',6),Object('Washer',1),Object('Bucket',1),Object('Mug',3),
    Object('Plant',2), Object('Clothes',7, ['Dry']), Object('Clothes',8, ['Dry']), Object('Clothes',9, ['Dry']), Object('Brush', 2), Object('Chair', 7),
            Object('Lamp', 9), Object('Book', 10, ['Red']), Object('Cupboard', 4)]
    rels = [Relation('Inside',objs[4], objs[3]),Relation('Inside',objs[5], objs[3])]
    dict1 = {}
    for obj in objs:
        dict1[obj.name] = obj
    dict2 = {}
    for rel in rels:
        dict2[rel.name] = rel
    l4 = Location('Washroom',1,dict1,dict2)
    robot = Robot()
    env = Environment({l1.name: l1, l2.name: l2, l3.name: l3, l4.name: l4}, robot, l1.name)
    return env

