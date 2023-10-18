from dsl import *

def prog_clean(prog):
    idx = 0
    for stmnt in prog.statements:
        if type(stmnt) is Goto or type(stmnt) is Foreach_obj:
            prog.statements[idx] = prog_clean(stmnt)

        if type(stmnt) is If:
            #Check if BEXP is true and add substatements to current list of statements
            if stmnt.bexp.tp == "True":
                pre_if_statements = prog.statements[0:idx]
                post_if_statements = prog.statements[(idx+1):]

                new_stmnt_list = pre_if_statements + stmnt.statements + post_if_statements

                prog.statements = new_stmnt_list

                return prog_clean(prog)

            #Check if next if statement has same bexp and combine
            if idx < len(prog.statements) - 1 and type(prog.statements[idx+1]) is If and stmnt.bexp == prog.statements[idx+1].bexp:
                stmnt.statements = stmnt.statements + prog.statements[idx+1].statements

                prog.statements.pop(idx+1)

                return prog_clean(prog)

            prog.statements[idx] = prog_clean(stmnt)

        idx += 1

    return prog