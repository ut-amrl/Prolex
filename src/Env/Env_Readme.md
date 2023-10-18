env_defs.py
    This contains lists of possible object, location, and relation types that can exist in an environment. Moreover, for
    Objects, this file indicates which properties and actions are valid for a given object type.

objects.py
    Contains the Object class which defines objects that exist in the environment. To keep track of state each Object
    has a type (based on available types in env_defs.py) and properties (based on available properties for the type 
    defined in env_defs.py). Each property is initialized to false.

relations.py
    Contains the Relation class which defines relations that currently exist in the environment. If a relation exists 
    that means that it is currently true. To keep track, each relation has a type (as defined in env_defs.py) and two
    objects for which the relation is defined.

locations.py
    Contains the Location class which defines the objects in the location, as well as the relations that currently hold.
    To keep track, each location has a dictionary of objects that currently exist within it (key values based on object
    name) and a dictionary for relations that currently hold within this locations (key values based on relation name).
    Whenever an object is removed from a location, all the corresponding relations are also removed. Within a location,
    objects can also be added, as well as removing and adding relations.

robot.py
    Contains the Robot class which is used to keep track of the objects held by the robot. To do this there is a 
    dictionary of objects (keyed with object name) to keep track of objects held by robot, which is initially empty. 
    Objects can be added and removed from the robot, which corresponds to picking up and putting down objects.

environment_state.py
    Contains the Environment class which is used to keep track of the current state of the environment. To do this, a 
    set of locations are saved in a dictionary which corresponds to all the locations in this environment instantiation.
    Each location contains the objects and respective locations within it. Also, a Robot is created to keep track of any
    objects that get picked up.

env_gen.py
    This script is used to generate random, initial symbolic environment states.