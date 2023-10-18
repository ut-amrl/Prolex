class XML_Node():
    def __init__(self, tp):
        self.tp = tp

        self.sub_nodes = []

    def print(self, indendent):
        tab = ''
        for i in range(indendent):
            tab = tab + '\t'

        if len(self.sub_nodes) > 0:
            print(tab + "<" + self.tp + ">")
            for node in self.sub_nodes:
                node.print(indendent + 1)

            print(tab + "</" + self.tp + ">")

        else:
            print(tab + "<" + self.tp + "> </" + self.tp + ">")