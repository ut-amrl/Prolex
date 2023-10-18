from Env.locations import Location
from Env.objects import Object
from Env.relations import Relation
from Env.environment_state import Environment
from Env.robot import Robot

import exp_config

import random
import sys
def gen_user_env():
    print("Welcome!")
    print("Environment definition allows these Location types: ")
    print(locations)
    print("Environment definition allows these Object types: ")
    print(object_types)
    print("Environment definition allows these relation types: ")
    print(relations)
    dict_locs = {}
    n_locs = int(input("Please enter number of rooms for this house: "))
    room_dict = {'Bedroom':0,'Kitchen':0,'Washroom':0,'Livingroom':0}
    for i in range(n_locs):
        room_type = input("Please enter the location type (Bedroom, Kitchen, Washroom, Livingroom): ")
        print("Please enter space separated object types and their props which are to hold true in separate lines: ")
        obj_dict = {'Fan':0, 'Stove':0, 'Chair':0, 'Table':0,'Cup':0}
        dict_objs = {}
        line = sys.stdin.read()
        contents = line.split("\n")
        for line in contents:
            li = line.split(" ")
            x = Object(li[0],obj_dict[li[0]])
            obj_dict[li[0]] += 1
            for j in range(len(li)-1):
                x.props[li[j+1]] = True
            dict_objs[x.name] = x            
        print("\nPlease enter relations that hold for this location on separate lines of the format (Relation_name Obj_1 Obj_2): ")
        line = sys.stdin.read()
        contents = line.split("\n")
        dict_rels = {}
        for rel in contents:
            rel_list = rel.split(" ")
            r = Relation(rel_list[0],dict_objs[rel_list[1]],dict_objs[rel_list[2]])
            dict_rels[r.name] = r
        l = Location(room_type,room_dict[room_type],dict_objs,dict_rels)
        dict_locs[l.name] = l
        room_dict[room_type] += 1
    robo_loc = input("Specify Robot's Initial location of the format Loc_1: ")
    robot = Robot()
    env = Environment(dict_locs, robot, robo_loc)
    return env

gen_user_env().print()

def gen_random_env():
    print("Welcome!")
    limit = {"Livingroom": {'Fan':1, 'Stove':0, 'Chair':2, 'Table':1,'Cup':2}, "Kitchen": {'Fan':1, 'Stove':1, 'Chair':4, 'Table':2,'Cup':5}, "Bedroom": {'Fan':1, 'Stove':0, 'Chair':1, 'Table':1,'Cup':2}}
    dict_locs = {}
    n_locs = int(input("Please enter number of rooms for this house: "))
    room_dict = {'Bedroom':0,'Kitchen':0,'Washroom':0,'Livingroom':0}
    for i in range(n_locs):
        if i==0:
            room_type = "Livingroom"
        elif i==1:
            room_type = "Kitchen"
        else:
            room_type = "Bedroom"
        obj_dict = {'Fan':0, 'Stove':0, 'Chair':0, 'Table':0,'Cup':0}
        dict_objs = {}
        for li in obj_dict:
            jj = random.randint(0,limit[room_type][li])
            if jj != 0:
                for k in range(jj):
                    x = Object(li,k)
                    obj_dict[li] += 1
                    for j in properties[li]:
                        x.props[j] = random.choice([True, False])
                dict_objs[x.name] = x  
        print("Objects randomly created for this location: ", obj_dict)          
        print("\nPlease enter relations that hold for this location on separate lines of the format (Relation_name Obj_1 Obj_2): ")
        line = sys.stdin.read()
        contents = line.split("\n")
        print(len(contents))
        dict_rels = {}
        for rel in contents:
            rel_list = rel.split(" ")
            r = Relation(rel_list[0],dict_objs[rel_list[1]],dict_objs[rel_list[2]])
            dict_rels[r.name] = r
        l = Location(room_type,room_dict[room_type],dict_objs,dict_rels)
        dict_locs[l.name] = l
        room_dict[room_type] += 1
    robo_loc = "Livingroom_0"
    robot = Robot()
    env = Environment(dict_locs, robot, robo_loc)
    return env

gen_random_env().print()