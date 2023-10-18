from demo import *
from dsl import *

def check(demo, prog, Initial_env, printing=True, exact=True):
    demo_execution = demo.execute(Initial_env)
    prog_execution = prog.execute(Initial_env)

    if exact:
        n = len(demo_execution[0])
        n1 = len(prog_execution[0])
        if n != n1:
            if printing:
                print("Program and Demonstartion are inconsistent.")
            return False
        for i in range(n):
            if not demo_execution[0][i].compare(prog_execution[0][i]):
                if printing:
                    print("ERROR: Program and Demonstartion are inconsistent.")
                    print("Program took action {}".format(prog_execution[1][i-1]))
                    print("Demonstration took action {}".format(demo_execution[1][i-1]))
                return
        if printing:
            print("Program and Demonstartion are consistent.")
        return True
    else: #Check only end state
        demo_end_state = demo_execution[0][-1]
        prog_end_state = prog_execution[0][-1]

        return demo_end_state == prog_end_state

def flatten_demo(demo):
    demo_str = demo.pretty_str(0)

    demo_stmnt_list = demo_str.split('\n')

    parsed_demo_stmnt_list = []
    for demo_stmnt in demo_stmnt_list:
        new_demo_stmnt = demo_stmnt.lstrip('\t')
        if new_demo_stmnt != '' and new_demo_stmnt.find('Demo') == -1:
            parsed_demo_stmnt_list.append(new_demo_stmnt)

    return parsed_demo_stmnt_list

def partial_exec(stmnts, Init_Env):
    exec_stmnts = []
    for stmnt in stmnts:
        if type(stmnt) is Goto:
            if stmnt.tp == "Goto":
                if stmnt.loc != None:
                    exec_stmnts.append(f'Goto( {stmnt.loc} ):')
                else:
                    return None
            # else: #Goto each expansion