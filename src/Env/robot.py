class Robot():
    def __init__(self) -> None:
        #Make location name based on type and num
        self.name = 'Robot'

        #Save objects that exist for this location
        #Init with empty dictionary
        self.objects = {}

    def __eq__(self, other):
        for obj in self.objects:
            found = False
            for o_obj in other.objects:
                if self.objects[obj] == other.objects[o_obj]:
                    found = True

            if not found:
                return False

        return True

    def add_object(self, object):
        """
        Adds an object to the robot's bag
        :param object: Object to be added
        :return: None
        """
        self.objects[object.name] = object

    def remove_object(self, object_name):
        """
        Removes object from the robot's bag
        :param object_name: Name of object to be removed from this location
        :return: Object being removed from this location
        """

        #Get the object to be removed
        removed_object =  self.objects.pop(object_name)

        return removed_object
    def get_object_types(self):
        l = [ ]
        for obj_name in self.objects:
            l.append(self.objects[obj_name].tp)
        return l
    def print(self, num_indent=0):
        indents=''
        for i in range(num_indent):
            indents = indents + '|\t'

        print(indents + self.name + ":")

        print(indents + '|\t Objects:')

        for object in self.objects:
            self.objects[object].print(num_indent=(num_indent+2))

    def perform_scan(self, obj_tp):
        l = []
        for obj_name in self.objects:
            if self.objects[obj_name].tp == obj_tp:
                l.append(obj_name)
        return l