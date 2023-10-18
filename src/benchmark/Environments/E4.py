from Env.objects import Object
from Env.relations import Relation
from Env.locations import Location
from Env.robot import Robot
from Env.environment_state import Environment
def E4():
    brush = Object('Brush',0)
    drawer = Object('Drawer',0)
    bed = Object('Bed',0)
    cloth0 = Object('Clothes',0)
    cloth1 = Object('Clothes',1)
    cloth2 = Object('Clothes',2)
    l1 = Location('Livingroom', 1, {drawer.name: drawer, brush.name: brush, bed.name:bed, cloth0.name:cloth0, cloth1.name: cloth1, cloth2.name:cloth2},{})
    fan5 = Object('Fan', 5)
    bed = Object('Bed',0)
    door = Object('Door',0)
    lamp0 = Object('Lamp',0)
    lamp1 = Object('Lamp',1)
    r1 = Relation('Near',lamp0,door)
    r2 = Relation('Near',lamp1,door)
    l5 = Location('Bedroom', 1,{fan5.name: fan5, bed.name: bed, door.name: door, lamp0.name: lamp0, lamp1.name: lamp1}, {r1.name: r1, r2.name: r2})
    robot = Robot()
    env = Environment({l1.name: l1, l5.name: l5}, robot, l1.name)
    return env