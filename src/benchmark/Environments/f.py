import sys
sys.path.append('../..')
sys.path.append('../../Env')
import exp_config

import random
from Env.objects import Object
from Env.relations import Relation
random.seed(42)
def f(env, n_objs, n_rels, n_beds=2):
    new_env = env
    new_beds = random.randint(0,n_beds)
    for i in range(new_beds):
        bed = env.locations['Bedroom_1']
        new_env.locations[bed.name] = bed
    for loc in new_env.locations:
        location = new_env.locations[loc]
        objs = random.choices(range(0, 40), k=random.randint(0,n_objs))
        idx = len(location.objects)
        for j in objs:
            #Make a set of random properties
            props_list = []
            for prop in exp_config.env_def.properties[exp_config.env_def.object_types[j]]:
                if random.randint(0, 100) % 2 == 0 and prop != "NoProp":
                    props_list.append(prop)
                    break

            obj = Object(exp_config.env_def.object_types[j],idx, props_list)
            idx += 1
            location.objects[obj.name]=obj
        rels = random.randint(0,n_rels)
        lis = list(location.objects.values())
        for j in range(rels):
            rel = random.choices(exp_config.env_def.relations,k=1)
            obj1 = random.choices(lis,k=1)
            obj2 = random.choices(lis,k=1)
            relation = Relation(rel[0],obj1[0],obj2[0])
            location.relations[relation.name] = relation
        new_env.locations[loc] = location
    return new_env

