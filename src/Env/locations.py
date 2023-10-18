from Env.relations import Relation
import exp_config
class Location():
    def __init__(self, tp, num, objects, relations) -> None:
        """

        :param tp: Type of location (e.g. Bedroom, Kitchen etc)
        :param num: Version number of this location type (e.g. 2nd bedroom created)
        :param objects: Dictionary of {object name: object} to initialize location with
        :param relations: Dictionary of {relation name: relation} on these objects to initialize location with
        """
        assert(tp in exp_config.env_def.locations)

        #Save Location type
        self.tp = tp

        #Make location name based on type and num
        self.name = tp + '_' + str(num)

        #Save objects that exist for this location
        self.objects = objects

        #Save relations that hold for this location
        self.relations = relations

    def __eq__(self, other):
        if self.tp != other.tp:
            return False

        if self.name != other.name:
            return False

        for objs in self.objects:
            found = False
            for o_objs in other.objects:
                if self.objects[objs] == other.objects[o_objs]:
                    found = True

            if not found:
                return False

        for rel in self.relations:
            found = False
            for o_rel in other.relations:
                if self.relations[rel] == other.relations[o_rel]:
                    found = True

            if not found:
                return False

        return True

    def add_object(self, object):
        """
        Adds an object to this location
        :param object: Object to be added
        :return: None
        """
        self.objects[object.name] = object

    def remove_object(self, object_name):
        """
        Removes object and all of its associated relations from this location
        :param object_name: Name of object to be removed from this location
        :return: Object being removed from this location
        """

        #Get the object to be removed
        if object_name in self.objects:
            removed_object =  self.objects.pop(object_name)

            #Remove all relations corresponding to this object since they no longer hold
            if removed_object != None:
                relations_to_remove = self.get_relations(object_name)

                for r in relations_to_remove:
                    self.remove_relation(r.name)

            return removed_object
        else:
            return None

    def get_relations(self, o1_name, o2_name=None):
        """
        Get all relations in this location that correspond to an object o1, and optionally a second object o2
        :param o1_name: Object name for which to return relations
        :param o2_name: Optional object name for which to return relations
        :return: Set of relations which correspond to o1_name (and optionally o2_name)
        """

        #o2_name not specified
        matcing_relations = []
        if o2_name == None:
            for key in self.relations:
                if o1_name in key:
                    matcing_relations.append(self.relations[key])

            return matcing_relations
        else:
            for key in self.relations:
                if o1_name in key and o2_name in key:
                    matcing_relations.append(self.relations[key])

            return matcing_relations

    def add_relation(self, relation):
        """
        Adds a new relation to the location once that relation holds
        :param relation: Relation to be added
        :return: None
        """

        self.relations[relation.name] = relation

    def remove_relation(self, relation_name):
        """
        Removes a relation from the dictionary of relations -- decision occurs externally, but the relation not existing
        implies that the relation no longer holds
        :param relation_name: Name of relation to be removed
        :return: None
        """

        self.relations.pop(relation_name)

    def print(self, num_indent=0):
        indents = ''
        for i in range(num_indent):
            indents = indents + '|\t'
        print("IsLocation(\"" + self.tp + "\")")
        # print(indents + "In " + self.name + ", we have the following:")

        # print(indents+ 'Objects:')

        for object in self.objects:
            print("IsIn( \""+ self.objects[object].name +"\", \"" + self.tp + "\")")
            self.objects[object].print(num_indent=0)
            
        # print(indents+ 'Following Relations hold for objects in this room:')

        for relation in self.relations:
            self.relations[relation].print(num_indent=0)
    
    def compare(self, loc):
        if self.name != loc.name:
            return False
        if len(self.objects) != len(loc.objects):
            return False
        if len(self.relations) != len(loc.relations):
            return False
        for o in self.objects:
            if not self.objects[o].compare(loc.objects[o]):
                return False
        for r in self.relations:
            if (r not in self.relations or
                r not in loc.relations or not self.relations[r].compare(loc.relations[r])):
                return False 
        return True
    
    def add_relations(self, obj, rel_set):
        """
        rel_set: [(rel_tp, obj2_name)]
        """
        for (tp,o2) in rel_set:
            if o2 in self.objects: #Incorrect object add from sketch, can't add relation
                new_rel = Relation(tp,obj,self.objects[o2])
                self.add_relation(new_rel)
        return
    
    def perform_scan(self, obj_tp):
        l = []
        for obj_name in self.objects:
            if self.objects[obj_name].tp == obj_tp:
                l.append(obj_name)
        return l
