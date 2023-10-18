import exp_config
class Relation():
    def __init__(self, tp, o1, o2) -> None:
        """
        Defines the objects and type of relation that holds true. E.g. tp='On', o1.name='Cup_1' and o2.name='Table_1'
        means that if this relation exists, then Cup_1 is on Table_1

        :param tp: Relation type (on, inside, beside, etc)
        :param o1: Object 1 in relation
        :param o2: Object 2 in relation
        """
        assert(tp in exp_config.env_def.relations)

        #Save relation type
        self.tp = tp

        #Objects involved in the relation
        self.o1 = o1
        self.o2 = o2

        # Name composed of tp, o1.name, o2.name
        self.name = self.tp + "_" + self.o1.name + "_" + self.o2.name

    def __eq__(self, other):
        if self.name == other.name:
            return True

        return False

    def print(self, num_indent=0):
        # Add number of indents
        indents = ''
        for i in range(num_indent):
            indents = indents + '|\t'
        # print(indents + self.o1.name + " is " + self.tp + " " + self.o2.name)
        print("HasRelation(\""+ self.o1.name +"\", \"" + self.o2.name +"\", \""+ self.tp + "\")")

    def compare(self, rel):
        if self.name != rel.name:
            return False
        return True
