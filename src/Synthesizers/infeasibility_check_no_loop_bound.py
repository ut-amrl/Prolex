from demo import *
from dsl import *

from benchmark.Tasks.B1 import *
from benchmark.Environments.E1 import *

from Synthesizers.demo_w_hole_gen import *
from Synthesizers.end_to_end_sketch_set_gen import *

variable_map = {}

def infeasible_no_loop_bound(prog, demo, env, exact=True):
    """

    :param prog: Partial (or complete) program to check feasibility against demonstration.
    :param demo: Demonstration to evaluate feasibility of prartial (or complete) program.
    :param env: Environment representing the initial state of execution to evaluate against.
    :return: True if the program is infeasible
    """

    #print(prog.pretty_str(0, debug=True))

    #Get order of operations taken by demo
    demo_ops = get_operation_order_demo(demo)

    #Get order of operations taken by partial program
    #If not possible return false since can't determine feasibility
    prog_trace = prog.partial_execute(env)[2]

    if prog_trace == None or prog_trace == []:
        return False

    prog_ops = get_operation_order_demo(prog_trace)

    if prog_ops == None:
        return False

    if exact:
        num_non_acts_seen = 0

        for i in range(len(prog_ops)):
            if prog_ops[i] == 'BROKEN':
                return True

            elif type(prog_ops[i]) is str:
                num_non_acts_seen += 1

                if prog_ops[i] == 'ONE TRUE':
                    continue

                #Check if obj instance in demo ops
                found = False
                for j in range(len(demo_ops)):
                    if type(demo_ops[j]) is Goto_stmnt:
                        continue
                    if demo_ops[j].action == "Place": #Check rel set
                        for rel in demo_ops[j].rel_set:
                            if rel[1] == prog_ops[i]:
                                found = True
                                break

                    if found:
                        break

                    elif demo_ops[j].obj_name == prog_ops[i]:
                        found = True
                        break

                if not found:
                    return True
            elif type(prog_ops[i]) is list:
                num_non_acts_seen += 1

                #Check that at least one of the scan types is used
                found = False
                not_mandatory = False
                if prog_ops[i][-1] == "NOT_MANDATORY":
                    not_mandatory = True
                for k in range(len(prog_ops[i])):
                    for j in range(len(demo_ops)):
                        if type(demo_ops[j]) is Goto_stmnt:
                            continue
                        if demo_ops[j].action == "Place":  # Check rel set
                            for rel in demo_ops[j].rel_set:
                                if rel[1] == prog_ops[i][k]:
                                    found = True
                                    break

                        if found:
                            break

                        elif demo_ops[j].obj_name == prog_ops[i][k]:
                            found = True
                            break

                    if found:
                        break

                if not found and not not_mandatory:
                    return True
                elif found and not_mandatory:
                    return True
            elif not prog_ops[i].partial_eq(demo_ops[i-num_non_acts_seen]):
                #Check if action is in rest of actions
                found = False
                for j in range(len(demo_ops)):
                    if prog_ops[i].partial_eq(demo_ops[j]):
                        found = True
                        break

                if not found:
                    return True

        return False
    else:
        for i in range(len(prog_ops)):
            #Check that action occurred
            found = False
            for j in range(len(demo_ops)):
                if prog_ops[i].partial_eq(demo_ops[j]):
                    found = True

            if not found:
                return True

        return False

def get_operation_order_demo(demo):
    """

    :param demo: Demonstration to get order of operations from.
    :return: List of operations taken in order.
    """
    operations = []
    for goto_stmnt in demo.statements:
        operations = operations + get_ops_order_demo_goto(goto_stmnt)

    return operations

def get_ops_order_demo_goto(goto_stmnt):
    """

    :param goto_stmnt: Goto statement to get sub statements of.
    :return: List of operations of sub statements of the goto statement
    """

    operations = []
    goto_stmnt_copy = deepcopy(goto_stmnt)
    goto_stmnt_copy.statements = []
    operations.append(goto_stmnt_copy)

    for stmnt in goto_stmnt.statements:
        if type(stmnt) is Goto_stmnt:
            operations = operations + get_ops_order_demo_goto(stmnt)
        elif type(stmnt) is Act_stmnt:
            operations.append(deepcopy(stmnt))
        elif type(stmnt) is str:# and stmnt == "BROKEN":
            operations.append(stmnt)
        elif type(stmnt) is list:
            operations.append(stmnt)

    return operations
