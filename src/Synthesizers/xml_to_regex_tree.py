import subprocess
from sys import platform
from Synthesizers.Defs.Regex import *

def xml_to_regex_tree(xml_file_path):
    """

    :param xml_file_path: File path to XML document to build Regex Tree from
    :return: Parsed regex tree dictionary based on XML schema learner
    """

    script_arg = 'schema-learn ' + xml_file_path
    if platform == 'win32':
        proc = subprocess.run(['C:\\Windows\\System32\\bash.exe', '-l', '-c', script_arg], capture_output=True)
    else:
        #print("Error " + platform + " not supported")

        #TODO: This code should work, but leaving in assertion until proven otherwise (don't have linux distro to check)
        proc = subprocess.run(['./share/XML-Schema-learner/schema-learn', xml_file_path], capture_output=True)

        #assert(1 == 0)

    #Parse output
    parse = proc.stdout.decode().split('\n')
    regex_dict = {}
    parsed_lines = []
    for line in parse:
        line = line.strip('<!ELEMENT')
        line = line.strip('>')
        line = line.split()
        if not line == [] and line[1] != "(#PCDATA)":
            parsed_lines.append(line)

    for line in parsed_lines:
        key = ''
        regex = ''
        for i in range(len(line)):
            if i == 0:
                key = line[i]
            else:
                regex = regex + ' ' + line[i]

        r_tree = make_tree(regex.split())
        regex_dict[key] = (regex, r_tree)

    return regex_dict

def combine_trees(key, tree1, tree2):
    #Check if tree root is key
    if tree1.tp == key:
        # Do insertion

        # Make new tree with same sub tree
        new_node = regexNode(tree1.tp)
        new_node.sub_tree = tree1.sub_tree

        tree1.tp = 'concat'
        tree1.sub_tree = []
        tree1.sub_tree.append(new_node)
        tree1.sub_tree.append(tree2)

        return True

    #Otherwise search tree1 one for key
    for regex_node in tree1.sub_tree:
        if regex_node.tp == key:
            #Do insertion

            #Make new tree with same sub tree
            new_node = regexNode(regex_node.tp)
            new_node.sub_tree = regex_node.sub_tree

            regex_node.tp = 'concat'
            regex_node.sub_tree = []
            regex_node.sub_tree.append(new_node)
            regex_node.sub_tree.append(tree2)

            return True
        else:
            #Recurse on sub_tree
            found = combine_trees(key, regex_node, tree2)

            if found != False:
                return found

    return False
