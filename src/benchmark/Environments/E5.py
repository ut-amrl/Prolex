from Env.objects import Object
from Env.relations import Relation
from Env.locations import Location
from Env.robot import Robot
from Env.environment_state import Environment
def E5():
    fridge = Object('Fridge',0)
    ct = Object('Counter',0)
    veggies0 = Object('Vegetable', 0)
    veggies1 = Object('Vegetable', 1)
    cereal = Object('Cereal',0)
    drawer = Object('Drawer',0)
    fruit0 = Object('Fruit',0)
    fruit1 = Object('Fruit',1)
    pot = Object('Pot', 0)
    pan = Object('Pan', 0)
    stove = Object('Stove', 0)
    r1 = Relation('Inside',fruit0, fridge)
    r3 = Relation('Inside',veggies0, fridge)
    r2 = Relation('Inside',fruit1, fridge)
    r4 = Relation('Inside',veggies1, fridge)
    table = Object('Table',0)
    dsh = Object('Dishwasher', 0)
    plate0 = Object('Plate',0)
    plate1 = Object('Plate',1)
    r3 = Relation('Inside', plate0, dsh)
    r4 = Relation('Inside', plate1, dsh)
    plant = Object('Plant',0)
    l1 = Location('Kitchen', 1, {pan.name: pan, r3.name: r3, r4.name: r4, plant.name: plant, dsh.name: dsh, table.name: table, plate0.name: plate0, plate1.name: plate1, pot.name: pot, stove.name: stove, fridge.name: fridge, ct.name: ct, fruit0.name: fruit0, fruit1.name: fruit1, veggies0.name: veggies0, veggies1.name: veggies1, drawer.name: drawer, cereal.name: cereal},{r1.name: r1, r2.name: r2, r3.name: r3, r4.name: r4})
    bucket = Object('Bucket',0)
    mug = Object('Mug',0)
    plant = Object('Plant',0)
    l2 = Location('Washroom', 0, {mug.name: mug, plant.name: plant, bucket.name: bucket}, {})
    robot = Robot()
    env = Environment({l1.name: l1, l2.name: l2}, robot, l1.name)
    return env