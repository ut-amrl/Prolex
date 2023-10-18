#Change this to change environment difficulty
#difficulty = "EASY"

#Specify the algorithm
#ALG_TYPE = ""
#INF_CHECK = False

#Value to change experiment timeout parameters
timeout_in_min = 2.0

#Num extra scans
extra_scans = 1

#Depth for extra nested object loops allowed
nested_obj_loops = 1

from Env import env_def as env_def_easy
from Env import env_def_med
from Env import env_def_hard


def init(diff):
    global env_def, extra_env_objs, extra_env_rels
    if diff == 'e':
        env_def = env_def_easy
        extra_env_objs = 0
        extra_env_rels = 0
    if diff == 'm':
        env_def = env_def_med
        extra_env_objs = 100
        extra_env_rels = 100
    if diff == 'h':
        env_def = env_def_hard
        extra_env_objs = 500
        extra_env_rels = 500
