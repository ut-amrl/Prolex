from Env.objects import Object
from Env.relations import Relation
from Env.locations import Location
from Env.robot import Robot
from Env.environment_state import Environment
def E3():
    fan1 = Object('Fan', 1)
    fan1.update_state("On", True)
    table0 = Object('Table', 0)
    cup_0 = Object('Cup', 0)
    cup_1 = Object('Cup', 1)
    cup_0.update_state("Full", True)
    stove_0 = Object('Stove', 0)

    r1 = Relation('On', cup_0, table0)
    r2 = Relation('Below', table0, cup_0)
    r3 = Relation('Above', cup_0, table0)

    r4 = Relation('On', cup_1, table0)
    r5 = Relation('Below', table0, cup_1)
    r6 = Relation('Above', cup_1, table0)

    l1 = Location('Kitchen', 0,
                  {table0.name: table0, fan1.name: fan1, cup_0.name: cup_0, cup_1.name: cup_1, stove_0.name: stove_0},
                  {r1.name: r1, r2.name: r2, r3.name: r3, r4.name: r4, r5.name: r5, r6.name: r6})

    robot = Robot()
    env = Environment({l1.name: l1}, robot, l1.name)
    return env