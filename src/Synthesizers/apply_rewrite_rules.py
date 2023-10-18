from Synthesizers.Defs.Regex import *
from copy import deepcopy

def rewrite_subtree_top(regex, regex_subtree):
    rewrites = rewrite_subtree(regex, regex_subtree)

    #Still need to potentially rewrite concats
    if rewrites == []:
        rewrites.append(regex)

    final_rewrite_set = []
    for rewrite in rewrites:
        # Get concat sub-tree rewrites apply only bottom up
        concat_nodes_list = []
        non_concat_node_list_count = 0
        sub_tree = [rewrite]
        while sub_tree != []:
            for node in sub_tree:
                if node.tp == "concat":
                    concat_nodes_list.append(node)
                else:
                    non_concat_node_list_count = non_concat_node_list_count + 1

            sub_tree = node.sub_tree

        # Bottom up so reverse order
        concat_nodes_list.reverse()
        final_rewrite_set.append(deepcopy(rewrite))

        for i in range(len(concat_nodes_list)):
            if i < len(concat_nodes_list) - 1:
                for j in range(len(concat_nodes_list[i].sub_tree)):
                    if j > 0:
                        concat_nodes_list[i + 1].sub_tree.append(concat_nodes_list[i].sub_tree[j])

                concat_nodes_list[i].tp = concat_nodes_list[i].sub_tree[0].tp
                concat_nodes_list[i].sub_tree = concat_nodes_list[i].sub_tree[0].sub_tree

                final_rewrite_set.append(deepcopy(rewrite))

    if non_concat_node_list_count == 0: #Can send back only last one since all concats
        return [final_rewrite_set[-1]]

    return final_rewrite_set

def rewrite_subtree(regex, regex_subtree, depth=[]):
    rewrite_set = []

    if len(regex_subtree) == 0:
        rewrite_set.append(regex)
        return rewrite_set

    #Check if all subtrees are empty
    check = True
    for regex_node in regex_subtree:
        if len(regex_node.sub_tree) != 0:
            check = False

    if check:
        rewrite_set.append(regex)
        return rewrite_set

    iter_count = 0
    for regex_node in regex_subtree:
        if regex_node.tp == "star" or regex_node.tp == "plus" or regex_node.tp == "concat" or regex_node.tp == '?':
            depth.append(iter_count)
            regex_node = regex
            for i in depth:
                regex_node = regex_node.sub_tree[i]

            rewrite_set = rewrite_set + rewrite_subtree(regex, regex_node.sub_tree, depth)
            depth.pop(-1)
        elif regex_node.tp == "or":
            depth.append(iter_count)

            regex_node = regex
            for i in depth:
                regex_node = regex_node.sub_tree[i]

            regex_node.tp = "concat"
            rewrite_set = rewrite_set + rewrite_subtree(regex, regex_node.sub_tree, depth)

            depth.pop(-1)

        iter_count = iter_count + 1

    return rewrite_set
