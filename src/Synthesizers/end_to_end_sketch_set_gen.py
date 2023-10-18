from Synthesizers.demo_to_xml import *
from Synthesizers.xml_to_regex_tree import *
from Synthesizers.apply_rewrite_rules import *
from Synthesizers.translate_regex_tree_to_sketch import *

from exp_config import *

import sys

def gen_sketch_set(demo, env):
    xml_base_path = ""

    #Get XML nodes for initial sketch set
    list_of_xml_node_list = demo_to_xml_node_top(demo.statements)

    # Print each in list to xml file and gather Regex Sets
    og_stdout = sys.stdout
    iter = 0
    rewrite_list_for_sketches = []
    for xml_node_list in list_of_xml_node_list:
        xml_path = xml_base_path + f'temp_{iter}.xml'
        iter += 1
        f = open(xml_path, 'w+')
        f.write('<demo>\n')
        sys.stdout = f
        for xml_node in xml_node_list:  # Need to write all separately
            xml_node.print(1)

        f.write('</demo>')
        f.close()

        sys.stdout = og_stdout

        #Get Regex rewrites
        regex_dict = xml_to_regex_tree(xml_path)

        # Apply rewrites to all
        rewrite_dict = {}
        for regex_name in regex_dict:
            rewrites = rewrite_subtree_top(regex_dict[regex_name][1], regex_dict[regex_name][1].sub_tree)

            rewrite_dict[regex_name] = (regex_dict[regex_name][0], rewrites)

        # Combine all rewrites
        for regex_name in rewrite_dict:
            for check_regex_name in rewrite_dict:
                if regex_name != check_regex_name and regex_name in rewrite_dict[check_regex_name][0]:
                    # Do the insertion into the regex tree

                    final_rewrite_set = []
                    for check_rewrite in rewrite_dict[check_regex_name][1]:
                        for rewrite in rewrite_dict[regex_name][1]:
                            tree1 = deepcopy(check_rewrite)
                            _ = combine_trees(regex_name, tree1, rewrite)

                            final_rewrite_set.append(tree1)

                    # Set regex in dict
                    rewrite_dict[check_regex_name] = (rewrite_dict[check_regex_name][0], final_rewrite_set)

        for rewrite in rewrite_dict['demo'][1]:
            rewrite_list_for_sketches.append(rewrite)


    sys.stdout = og_stdout

    #Do translation
    sketches = []
    iter = 0
    for rewrite in rewrite_list_for_sketches:
        sketch_stmnts = translate_regex_tree_to_sub_sketch(rewrite, {}, {})

        if sketch_stmnts != None:
            sketch = Prog(iter)
            iter += 1

            for stmnt in sketch_stmnts:
                sketch.statements.append(stmnt)

            sketches.append(sketch)

    #Remove any duplicates
    remove_idx_set = set()
    for i in range(len(sketches)):
        for j in range(len(sketches)):
            if i < j and sketches[i] == sketches[j]:
                remove_idx_set.add(j)

    #Must do in reverse order
    idx_list = []
    for idx in remove_idx_set:
        idx_list.append(idx)

    idx_list.sort(reverse=True)

    for idx in idx_list:
        sketches.pop(idx)

    #Add scans to each sketch depending on scan depth
    added_sketches = []
    for sketch in sketches:
        for i in range(extra_scans):
            new_sketch = deepcopy(sketch)

            #Add i scans and lets
            for j in range(i + 1):
                os = object_set()
                new_scan = Scan(None, os)

                v = variable(None)
                new_let = Let(v, None, None)

                #Add new scan/let into every goto
                for stmnt in new_sketch.statements:
                    stmnt.statements = [deepcopy(new_scan), deepcopy(new_let)] + stmnt.statements

            added_sketches.append(new_sketch)

    sketches += added_sketches

    #Add nested object for loops to each depending on for loop depth
    added_sketches = []
    for sketch in sketches:
        #Get foreach_obj positions
        foreach_obj_locs = []
        goto_idx = 0
        for goto in sketch.statements:
            stmnt_idx = 0
            for stmnt in goto.statements:
                if type(stmnt) is Foreach_obj:
                    foreach_obj_locs.append((goto_idx, stmnt_idx))

                stmnt_idx += 1

            goto_idx += 1

        #Get all combinations of foreach_objs
        foreach_obj_loc_sets = cartesian_product_of_foreach_objs(foreach_obj_locs)

        for tuple_set in foreach_obj_loc_sets:
            new_sketch = deepcopy(sketch)
            for tuple in tuple_set:
                for i in range(nested_obj_loops):
                    # Add i foreach nesting
                    for j in range(i + 1):
                        iter = Iterator()
                        new_foreach = Foreach_obj(iter, None)
                        new_foreach.statements.append(new_sketch.statements[tuple[0]].statements[tuple[1]])

                        new_sketch.statements[tuple[0]].statements[tuple[1]] = new_foreach

            added_sketches.append(new_sketch)

    sketches += added_sketches

    # Remove any duplicates
    remove_idx_set = set()
    for i in range(len(sketches)):
        for j in range(len(sketches)):
            if i < j and sketches[i] == sketches[j]:
                remove_idx_set.add(j)

    # Must do in reverse order
    idx_list = []
    for idx in remove_idx_set:
        idx_list.append(idx)

    idx_list.sort(reverse=True)

    for idx in idx_list:
        sketches.pop(idx)

    return sketches

def cartesian_product_of_foreach_objs(foreach_obj_locs):
    if len(foreach_obj_locs) == 0:
        return []
    if len(foreach_obj_locs) == 1:
        return [foreach_obj_locs]

    ret_list = []
    idx = 0
    for loc in foreach_obj_locs:
        ret_list.append([loc])
        after_pairs = cartesian_product_of_foreach_objs(foreach_obj_locs[idx+1:])
        ret_list += after_pairs

        for prod in after_pairs:
            new_prod = deepcopy(prod)
            new_prod.append(loc)

            ret_list.append(new_prod)

        idx += 1

    return ret_list
