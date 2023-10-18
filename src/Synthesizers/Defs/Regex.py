class regexNode():
    def __init__(self, tp):
        self.tp = tp

        self.sub_tree = []

    def print(self, indendent):
        tab = ''
        for i in range(indendent):
            tab = tab + '|\t'
        print(tab + self.tp)
        for sub_tree in self.sub_tree:
            sub_tree.print(indendent + 1)

def make_tree(regex):
    if regex[0] == '(#PCDATA)':
        return None
    elif len(regex) == 1:
        if regex[0].endswith('*'):
            node = regexNode('star')
            sub_tree = make_tree([regex[0].strip('*')])
            node.sub_tree.append(sub_tree)

            return node

        elif regex[0].endswith('+'):
            node = regexNode('plus')
            sub_tree = make_tree([regex[0].strip('+')])
            node.sub_tree.append(sub_tree)

            return node

        else:
            return regexNode(regex[0])

    elif regex[0] == '(':
        #Find index with ')'
        idx = 0
        for i in range(len(regex)):
            if regex[i].find(')') != -1 and regex[1] != '(' and regex[-1] != ')':
                idx = i
                break

        if regex[idx].find(',') != -1:
            node = regexNode('concat')

            left_regex = regex[0:idx+1]
            left_regex[-1] = left_regex[-1].strip(',')
            left = make_tree(left_regex)
            right = make_tree(regex[idx+1:])

            node.sub_tree.append(left)
            node.sub_tree.append(right)

            return node
        elif regex[idx].find(')*') != -1:
            node = regexNode('star')
            sub_tree = make_tree(regex[1:idx])
            node.sub_tree.append(sub_tree)

            return node
        elif regex[idx].find(')+') != -1:
            node = regexNode('plus')
            sub_tree = make_tree(regex[1:idx])
            node.sub_tree.append(sub_tree)

            return node

        else:
            return make_tree(regex[1:-1])

    elif regex[0] == '#PCDATA':
        return make_tree(regex[2:])

    else:
        if regex[1] == '|':
            node = regexNode('or')

            left = make_tree(regex[:1])
            right = make_tree(regex[2:])

            if right == None:
                assert 1 == 0

            node.sub_tree.append(left)
            node.sub_tree.append(right)

            return node

        elif regex[0].endswith(','):
            node = regexNode('concat')

            left = make_tree([regex[0].strip(',')])
            right = make_tree(regex[1:])

            node.sub_tree.append(left)
            node.sub_tree.append(right)

            return node