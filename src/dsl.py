from demo import *
variable_map = {}
class Prog:
    def __init__(self, id) -> None:
        self.id = id
        self.statements = list()
    def add_stmnt(self, stmnt):
        # assert(isinstance(stmnt, Goto))
        self.statements.append(stmnt)

    #For priority queue to allow comparison between Prog objects for tie breaking priority
    def __lt__(self, other):
        return True

    def pretty_str(self, indent=0, debug=False) -> String:
        res = 'Program_'+str(self.id)+":\n"
        for stmnt in self.statements:
            res += stmnt.pretty_str(indent, debug)
        return res
    def execute(self, state):
        global variable_map
        variable_map["L"] = state.locations.keys()
        l = [state]
        a = []
        demo = Demo(0)
        s = deepcopy(state)
        for stmnt in self.statements:
            temp = stmnt.execute(s)
            l += temp[0]
            a += temp[1]
            for ss in  temp[2]:
                demo.add_stmnt(ss)
            if len(l) != 0:
                s = deepcopy(l[-1])
        return (l,a, demo)

    def partial_execute(self, state):
        global variable_map
        variable_map["L"] = state.locations.keys()
        l = [state]
        a = []
        demo = Demo(0)
        s = deepcopy(state)
        for stmnt in self.statements:
            temp = stmnt.partial_execute(s)
            l += temp[0]
            a += temp[1]
            for ss in  temp[2]:
                demo.add_stmnt(ss)
            if len(l) != 0:
                s = deepcopy(l[-1])
        return (l,a, demo)

    #Equality to check for sketch duplicates
    def __eq__(self, other):
        if type(self) != type(other):
            return False

        if len(self.statements) != len(other.statements):
            return False

        for i in range(len(self.statements)):
            if self.statements[i] != other.statements[i]:
                return False

        return True

class Goto:
    def __init__(self,tp,loc=None, itr=None) -> None:
        self.tp = tp 
        self.loc = loc
        self.itr = itr
        self.statements = list()
    def add_stmnt(self, stmnt):
        self.statements.append(stmnt)
    def pretty_str(self, indent=0, debug=False) -> String:
        res = ''
        if self.tp=='Goto':
            if self.loc == None:
                res += 'Goto( ' + '?' + " ):\n"
            else:
                res += 'Goto( ' + self.loc.get_name() + " ):\n"
        else:
            res += 'Goto_each( ' + self.itr.pretty_str(0, debug) + " in L ):\n"
        s = ''
        for i in range(indent+1):
            s += '\t'
        for stmnt in self.statements:
            res += s + stmnt.pretty_str(indent+1, debug)
        return res
    def nl(self):
        loc_to_check = "[MASK]"
        holes_present = 1
        if self.loc!= None:
            loc_to_check = self.loc.pretty_str(0).split('_')[0]
            holes_present = 0

        return f"Go to the {loc_to_check}", holes_present
    def execute(self, state):
        assert (self.tp in {'Goto', 'Goto_each'})
        global variable_map
        if self.tp == 'Goto':
            goto = Goto_stmnt(self.loc.pretty_str(0))
            state.update_robot_loc(self.loc.pretty_str(0))
            l = [state]
            a = ['Goto( ' + self.loc.pretty_str(0) + " )"]
            s = deepcopy(state)      
            for stmnt in self.statements:
                temp = stmnt.execute(s)
                if temp != None:
                    l += temp[0]
                    a += temp[1]
                    for ss in  temp[2]:
                        goto.add_stmnt(ss)
                    if len(l) != 0:
                        s = deepcopy(l[-1])
            lis = [goto]
        else:
            l = []
            a = []
            lis = []
            s = deepcopy(state)
            for i in range(len(variable_map["L"])):
                variable_map[self.itr.pretty_str(0)] = list(variable_map["L"])[i]
                goto = Goto_stmnt(list(variable_map["L"])[i])
                s.update_robot_loc(list(variable_map["L"])[i])
                l += [deepcopy(s)] 
                a += ['Goto( ' + list(variable_map["L"])[i] + " )"]               
                for stmnt in self.statements:
                    temp = stmnt.execute(s)
                    l += temp[0]
                    a += temp[1]
                    for ss in  temp[2]:
                        goto.add_stmnt(ss)
                    if len(l) != 0:
                        s = deepcopy(l[-1])
                lis.append(goto)
        return (l,a, lis)

    def partial_execute(self, state):
        if self.tp not in ['Goto', 'Goto_each'] or (self.loc == None and self.itr == None):
            return [], [], []
        global variable_map
        if self.tp == 'Goto':
            goto = Goto_stmnt(self.loc.pretty_str(0))
            state.update_robot_loc(self.loc.pretty_str(0))
            l = [state]
            a = ['Goto( ' + self.loc.pretty_str(0) + " )"]
            s = deepcopy(state)
            for stmnt in self.statements:
                temp = stmnt.partial_execute(s)
                if temp != None:
                    l += temp[0]
                    a += temp[1]
                    for ss in  temp[2]:
                        goto.add_stmnt(ss)
                    if len(l) != 0:
                        s = deepcopy(l[-1])
            lis = [goto]
        else:
            l = []
            a = []
            lis = []
            s = deepcopy(state)
            for i in range(len(variable_map["L"])):
                variable_map[self.itr.pretty_str(0)] = list(variable_map["L"])[i]
                goto = Goto_stmnt(list(variable_map["L"])[i])
                s.update_robot_loc(list(variable_map["L"])[i])
                l += [deepcopy(s)]
                a += ['Goto( ' + list(variable_map["L"])[i] + " )"]
                for stmnt in self.statements:
                    temp = stmnt.partial_execute(s)
                    if temp != None:
                        l += temp[0]
                        a += temp[1]
                        for ss in  temp[2]:
                            goto.add_stmnt(ss)
                        if len(l) != 0:
                            s = deepcopy(l[-1])
                lis.append(goto)
        return (l,a, lis)

    # Equality to check for sketch duplicates
    def __eq__(self, other):
        if type(self) != type(other):
            return False

        if self.tp != other.tp:
            return False

        if self.loc != other.loc:
            return False

        if len(self.statements) != len(other.statements):
            return False

        for i in range(len(self.statements)):
            if self.statements[i] != other.statements[i]:
                return False

        return True

class Scan:
    def __init__(self, obj_tp, obj_set) -> None:
        self.obj_tp = obj_tp
        self.init_type = obj_tp
        self.obj_set = obj_set
        self.obj_tp_hole = False
    def pretty_str(self, indent=0, debug=False) -> String:
        res = ''
        if self.obj_tp == None:
            res += self.obj_set.pretty_str(indent, debug) + ' = Scan( ' + '?' + " )\n"
        else:
            res += self.obj_set.pretty_str(indent, debug) + ' = Scan( ' + str(self.obj_tp) + " )\n"
        return res
    def execute(self, state):
        assert (type(self.obj_tp) is str)
        # assert (self.obj_tp in env_def.object_types)
        global variable_map
        lis = state.find_loc(state.robot_loc).perform_scan(self.obj_tp)

        # Also include robot held objects in returned set
        lis = state.robot.perform_scan(self.obj_tp) + lis

        variable_map[self.obj_set.pretty_str(0)] = lis

        #no more scans in demo
        #scan = Scan_stmnt(self.obj_tp, self.obj_tp_hole)
        l = []
        a = []
        return (l, a, [])

    def partial_execute(self, state):
        if type(self.obj_tp) is not str:
            return [], [], []

        global variable_map
        lis = state.find_loc(state.robot_loc).perform_scan(self.obj_tp)

        # Also include robot held objects in returned set
        lis = state.robot.perform_scan(self.obj_tp) + lis

        variable_map[self.obj_set.pretty_str(0)] = lis
        #scan = Scan_stmnt(self.obj_tp, self.obj_tp_hole)
        l = []
        a = []
        if lis != []:
            if self.init_type != None:
                lis = [lis]
            else:
                lis.append('NOT_MANDATORY')
                lis = [lis]
        return (l, a, lis)

    def nl(self):
        obj_to_check = "[MASK]"
        holes_present = 1
        if self.obj_tp != None:
            obj_to_check = str(self.obj_tp)
            holes_present = 0

        return f"Look for a {obj_to_check}", holes_present
    def fill_hole(self, ctx0, ctx1,hole="obj", others=None):
        s = "Look for a [MASK]"
        for stmnt in ctx0:
            s = stmnt + " and " + s
        for stmnt in ctx1:
            s = s + " and " + stmnt
        return s, env_def.object_types


    #For checking duplicate sketches
    def __eq__(self, other):
        if type(self) != type(other):
            return False

        if self.obj_tp != other.obj_tp:
            return False

        return True

class Let:
    def __init__(self, v, v_bar, i, obj_tp=None, inst=0) -> None:
        self.v = v
        self.v_bar = v_bar
        self.i = i
        self.obj_tp = obj_tp
        self.inst = inst
    def pretty_str(self, indent=0, debug=False) -> String:
        res = ''
        v_to_print = ''
        v_bar_to_print = ''
        i_to_print = ''
        if self.v == None:
            v_to_print = '?'
        else:
            v_to_print = self.v.pretty_str(indent, debug)

        if self.v_bar == None:
            v_bar_to_print = '?'
        else:
            v_bar_to_print = self.v_bar.pretty_str(indent, debug)

        if self.i == None:
            i_to_print = '?'
        else:
            i_to_print = str(self.i)

        if self.obj_tp == None:
            obj_tp_to_print = '?'
        else:
            obj_tp_to_print = self.obj_tp

        if debug:
            res += 'Let ' + v_to_print + ' = ' + v_bar_to_print + "[" + i_to_print + "]" + "LET OF TYPE: " + obj_tp_to_print +'\n'
        else:
            res += 'Let ' + v_to_print + ' = ' + v_bar_to_print + "[" + i_to_print + "]\n"

        return res
    def execute(self, state):
        global variable_map
        if self.i < len(list(variable_map[self.v_bar.pretty_str(0)])):
            variable_map[self.v.pretty_str(0)] = list(variable_map[self.v_bar.pretty_str(0)])[self.i]
        else:
            variable_map[self.v.pretty_str(0)] = None
        # let = Let_stmnt(self.v, self.v_bar, self.i)
        l = []
        a = []
        return (l, a, [])

    def partial_execute(self, state):
        global variable_map
        if self.v_bar == None or self.i == None:
            return [], [], []

        l = []
        a = []
        lis = []
        if self.i < len(list(variable_map[self.v_bar.pretty_str(0)])):
            variable_map[self.v.pretty_str(0)] = list(variable_map[self.v_bar.pretty_str(0)])[self.i]

            #PUT OBJ INSTANCE HERE if type known => Mandatory Let
            if self.obj_tp != None:
                lis = [self.v.get_name()]
        else:
            variable_map[self.v.pretty_str(0)] = None
            lis = ['BROKEN']

        return (l, a, lis)

    #For removing duplicate sketches
    def __eq__(self, other):
        if type(self) != type(other):
            return False

        if self.obj_tp != other.obj_tp:
            return False

        return True

class If:
    def __init__(self, bexp) -> None:
        self.bexp = bexp
        self.statements = list()
    def add_stmnt(self,stmnt):
        self.statements.append(stmnt)

    def pretty_str(self, indent=0, debug=False) -> String:
        res = ''
        if self.bexp == None:
            res += 'If ( ' + '?' + " ):\n"
        else:
            res += 'If ( ' + self.bexp.pretty_str(0, debug) + " ):\n"
        s = ''
        for i in range(indent+1):
            s += '\t'
        for stmnt in self.statements:
            res += s + stmnt.pretty_str(indent+1, debug)
        return res
    def execute(self,state):
        l = []
        a = []
        lis = []
        #No checks in demo
        # for ss in  self.bexp.to_demo():
        #     lis.append(ss)
        if self.bexp.eval(state):
            s = deepcopy(state)
            for stmnt in self.statements:
                temp = stmnt.execute(s)
                if temp != None:
                    l += temp[0]
                    a += temp[1]
                    for ss in  temp[2]:
                        lis.append(ss)
                    if len(l) != 0:
                        s = deepcopy(l[-1])
        return (l, a, lis)

    def partial_execute(self,state):
        l = []
        a = []
        lis = []
        if self.bexp == None:
            return (l, a, lis)
        # for ss in self.bexp.to_demo():
        #     lis.append(ss)
        if self.bexp.partial_eval(state) == None:
            return None
        elif self.bexp.partial_eval(state):
            s = deepcopy(state)
            for stmnt in self.statements:
                temp = stmnt.partial_execute(s)
                if temp != None:
                    l += temp[0]
                    a += temp[1]
                    if temp[2] == []:
                        lis.append('ONE TRUE')
                    for ss in  temp[2]:
                        lis.append(ss)
                    if len(l) != 0:
                        s = deepcopy(l[-1])
        else:
            lis = ['FALSE']
        return (l, a, lis)

    def nl(self):
        if self.bexp != None:
            return self.bexp.nl()
        else:
            return "", 0

    #For removing duplicate sketches
    def __eq__(self, other):
        if type(self) != type(other):
            return False

        if self.bexp != other.bexp:
            return False

        if len(self.statements) != len(other.statements):
            return False

        for i in range(len(self.statements)):
            if self.statements[i] != other.statements[i]:
                return False

        return True

class Bexp:
    def __init__(self, tp, right, left = None) -> None:
        self.tp = tp
        self.left = left
        self.right = right
    def pretty_str(self, indent=0, debug=False) -> String:
        res = ''
        if self.left == None:
            l_to_print = '?'
        else:
            l_to_print = self.left.pretty_str(0, debug)

        if self.right == None:
            r_to_print = '?'
        else:
            r_to_print = self.right.pretty_str(0, debug)

        if self.tp == 'or':
            res += '('+ l_to_print + ' ) \/ (' + r_to_print + ')'
        elif self.tp == 'neg':
            res += '~' + '(' + r_to_print + ')'
        elif self.tp == 'and':
            res += '(' + l_to_print + ") /\ (" + r_to_print +')'
        elif self.tp == 'True':
            res += '( True )'
        elif self.tp == 'False':
            res += '( False )'
        else:
            if self.right != None and self.left != None:
                res += '(' + l_to_print + ") ? (" + r_to_print +')'
            elif self.right != None:
                res += r_to_print
            else:
                res += '?'
        return res
    def to_demo(self):
        lis = []
        if self.tp == "or" or self.tp == "and":
            if self.right == None or self.left == None:
                return []

            right_demo = self.right.to_demo()
            left_demo = self.left.to_demo()

            if right_demo == [] or left_demo == []:
                return []

            lis.append(Bexp_stmnt('single', right_demo[0]))
            lis.append(Bexp_stmnt('single', left_demo[0]))
        else:
            if self.right == None:
                return []

            right_demo = self.right.to_demo()
            if right_demo == []:
                return []

            lis.append(Bexp_stmnt('single', right_demo[0]))

        return lis
    def eval(self, state):
        assert (self.tp in {'or', 'and', 'neg', 'single', 'True', 'False'})

        if self.tp == 'True':
            return True
        if self.tp == 'False':
            return False

        if self.tp == 'or':
            return (self.left.eval(state) or self.right.eval(state))
        elif self.tp == 'and':
            return (self.left.eval(state) and self.right.eval(state))
        elif self.tp == 'neg':
            return (not self.right.eval(state))
        else:
            return self.right.eval(state)

    def partial_eval(self, state):
        if self.tp not in ['or', 'and', 'neg', 'single']:
            if self.tp == 'True':
                return True
            return False
        if self.tp == 'or':
            if self.left == None or self.right == None:
                return False
            return (self.left.partial_eval(state) or self.right.partial_eval(state))
        elif self.tp == 'and':
            if self.left == None or self.right == None:
                return False
            return (self.left.partial_eval(state) and self.right.partial_eval(state))
        elif self.tp == 'neg':
            if self.right == None:
                return False
            return (not self.right.partial_eval(state))
        else:
            if self.right == None:
                return False
            return self.right.partial_eval(state)

    def nl(self):
        sentence = ""
        holes_present = 0

        if self.left != None:
            temp_sentence, temp_holes = self.left.nl()

            sentence = sentence + temp_sentence
            holes_present = holes_present + temp_holes

        if self.right != None:
            temp_sentence, temp_holes = self.right.nl()

            sentence = sentence + temp_sentence
            holes_present = holes_present + temp_holes

        return sentence, holes_present

    #For removing duplicate sketches
    def __eq__(self, other):
        if type(self) != type(other):
            return False

        if self.tp != other.tp:
            return False

        if self.right != other.right:
            return False

        if self.left != other.left:
            return False

        return True

class Check_prop:
    def __init__(self, obj, obj_prop, obj_tp) -> None:
        self.obj = obj
        self.obj_prop = obj_prop
        self.obj_tp = obj_tp

        self.obj_prop_hole = False
        self.obj_tp_hole = False
    def pretty_str(self, indent=0, debug=False) -> String:
        res = ''

        obj_to_print = ''
        if self.obj == None:
            obj_to_print = '?'
        else:
            obj_to_print = self.obj.pretty_str(0, debug)

        if self.obj_prop == None:
            obj_prop_to_print = '?'
        else:
            obj_prop_to_print = self.obj_prop

        if debug:
            res += 'Check_prop( ' + obj_to_print + ', ' + obj_prop_to_print + ' )' + "CHECKING " + obj_to_print
        else:
            res += 'Check_prop( ' + obj_to_print + ', ' + obj_prop_to_print + ' )'

        return res
    def to_demo(self):
        if self.obj == None or self.obj_prop == None:
            return []
        check = Check_prop_pred(self.obj.get_name(),self.obj_prop, self.obj_tp_hole, self.obj_prop_hole)
        return [check]
    def eval(self, state):
        #assert (type(self.obj_prop) is str)
        if self.obj == None:
            assert 1 == 0
        obj_name = self.obj.get_name()
        if obj_name != None and state.find_object(obj_name) != None:
            return state.find_object(obj_name).check_prop(self.obj_prop)
        else:
            return False

    def partial_eval(self, state):
        #assert (type(self.obj_prop) is str)
        if self.obj == None:
            return None
        obj_name = self.obj.get_name()
        if obj_name != None and self.obj_prop != None and state.find_object(obj_name) != None:
            return state.find_object(obj_name).check_prop(self.obj_prop)
        else:
            return None
    def nl(self):
        holes_present = 2
        prop_to_check = "[MASK]"
        obj_to_check = "[MASK]"

        if self.obj != None:
            obj_to_check = self.obj.get_name()
            holes_present = holes_present -1

        if self.obj_prop != None:
            prop_to_check = self.obj_prop
            holes_present = holes_present - 1

        return f"Check if {obj_to_check} is {prop_to_check}", holes_present
    def fill_hole(self,ctx0, ctx1, hole, others=None):
        if hole=="prop":
            l = f"Check if {others[0]} is [MASK]"
            fills = env_def.properties[others[0]]
        elif  hole=="obj":
            l = f"Check if [MASK] is {others[0]}"
            fills = end_def.props[others[0]]
        for s in l:
            for stmnt in ctx0:
                s = stmnt + " and " + s
            for stmnt in ctx1:
                s = s + " and " + stmnt
        return l, fills

    #For removing duplicate sketches
    def __eq__(self, other):
        if type(self) != type(other):
            return False

        if self.obj_tp != other.obj_tp:
            return False

        if self.obj_prop != other.obj_prop:
            return False

        return True


class Check_rel:
    def __init__(self, obj1, obj2, rel, obj1_tp, obj2_tp) -> None:
        self.obj1 = obj1
        self.obj2 = obj2
        self.rel = rel
        self.obj1_tp = obj1_tp
        self.obj2_tp = obj2_tp

        self.rel_hole = False
        self.obj1_tp_hole = False
        self.obj2_tp_hole = False
    def pretty_str(self, indent=0, debug=False) -> String:
        res = ''

        obj1_to_print = ''
        obj2_to_print = ''
        rel_to_print = ''

        if self.obj1 == None:
            obj1_to_print = '?'
        else:
            obj1_to_print = self.obj1.pretty_str(0, debug)

        if self.obj2 == None:
            obj2_to_print = '?'
        else:
            obj2_to_print = self.obj2.pretty_str(0, debug)

        if self.rel == None:
            rel_to_print = '?'
        else:
            rel_to_print = self.rel

        if debug:
            res += 'Check_rel( ' + obj1_to_print + ', ' + obj2_to_print + ', ' + rel_to_print + ' )' + "CHECKING " + obj1_to_print + " and " + obj2_to_print
        else:
            res += 'Check_rel( ' + obj1_to_print + ', ' + obj2_to_print + ', ' + rel_to_print + ' )'

        return res
    def to_demo(self):
        if self.obj1 == None or self.obj2 == None or self.rel == None:
            return []
        check = Check_rel_pred(self.obj1.get_name(),self.obj2.get_name(),self.rel, self.obj1_tp_hole, self.obj2_tp_hole, self.rel_hole)
        return [check]
    def eval(self, state):
        if type(self.rel) is not str:
            assert 1 == 0
        assert (type(self.rel) is str)
        if self.obj1.get_name() is None or self.obj2.get_name() is None:
            return False
        return state.check_rel(self.rel + "_" + self.obj1.get_name() + "_" + self.obj2.get_name())

    def partial_eval(self, state):
        if type(self.rel) is not str or self.obj1 == None or self.obj2 == None:
            return False

        obj1_name = self.obj1.get_name()
        obj2_name = self.obj2.get_name()
        if obj1_name != None and obj2_name != None:
            return state.check_rel(self.rel + "_" + obj1_name + "_" + obj2_name)
        else:
            return False

    def nl(self):
        holes_present = 3
        obj1_to_check = "[MASK]"
        obj2_to_check = "[MASK]"
        rel_to_check = "[MASK]"

        if self.obj1 != None:
            obj1_to_check = self.obj1.get_name()
            holes_present = holes_present - 1

        if self.obj2 != None:
            obj2_to_check = self.obj2.get_name()
            holes_present = holes_present - 1

        if self.rel != None:
            rel_to_check = self.rel
            holes_present = holes_present - 1

        return f"Check if {obj1_to_check} is {rel_to_check} {obj2_to_check}", holes_present
    def fill_hole(self,ctx0, ctx1, hole, others=None):
        if hole == "rel":
            l = f"Check if {others[0]} is [MASK] {others[1]}"
            fills = env_def.relations
        elif  hole == "obj1":
            l = f"Check if [MASK] is {others[0]} {others[1]}"
            fills = end_def.object_types
        elif  hole == "obj2":
            l = f"Check if {others[0]} is {others[1]} [MASK]"
            fills = env_def.object_types
        for s in l:
            for stmnt in ctx0:
                s = stmnt + " and " + s
            for stmnt in ctx1:
                s = s + " and " + stmnt
        return l, fills

    #For removing duplicate sketches
    def __eq__(self, other):
        if type(self) != type(other):
            return False

        if self.obj1_tp != other.obj1_tp:
            return False

        if self.obj2_tp != other.obj2_tp:
            return False

        if self.rel != other.rel:
            return False

        return True

class Foreach_obj:
    def __init__(self, itr, obj_set) -> None:
        self.itr = itr
        self.obj_set = obj_set
        self.statements = list()
    def add_stmnt(self,stmnt):
        self.statements.append(stmnt)

    def pretty_str(self, indent=0, debug=False) -> String:
        res = ''

        itr_to_print = ''
        obj_set_to_print = ''
        if self.itr == None:
            itr_to_print = '?'
        else:
            itr_to_print = self.itr.pretty_str(0, debug)

        if self.obj_set == None:
            obj_set_to_print = '?'
        else:
            obj_set_to_print = self.obj_set.pretty_str(0, debug)

        res += 'For each ' + itr_to_print +' in ' + obj_set_to_print + ':\n'
        s = ''
        for i in range(indent+1):
            s += '\t'
        for stmnt in self.statements:
            res += s + stmnt.pretty_str(indent+1, debug)
        return res
    def execute(self, state):
        global variable_map
        lis = variable_map[self.obj_set.pretty_str(0)]
        l = []
        a = []
        liss = []
        s = deepcopy(state)
        for i in range(len(lis)):
            variable_map[self.itr.pretty_str(0)] = lis[i]
            for stmnt in self.statements:
                temp = stmnt.execute(s)
                if temp != None:
                    l += temp[0]
                    a += temp[1]
                    for ss in  temp[2]:
                        liss.append(ss)
                    if len(l) != 0:
                        s = deepcopy(l[-1])
        return (l, a, liss)

    def partial_execute(self, state):
        global variable_map
        if self.obj_set == None:
            return [], [], []
        lis = variable_map[self.obj_set.pretty_str(0)]
        l = []
        a = []
        liss = []
        s = deepcopy(state)

        stmnt_false_cnt = []
        for i in range(len(self.statements)):
            stmnt_false_cnt.append(0)

        for i in range(len(lis)):
            variable_map[self.itr.pretty_str(0)] = lis[i]
            stmnt_idx = 0
            for stmnt in self.statements:
                temp = stmnt.partial_execute(s)
                if temp != None:
                    l += temp[0]
                    a += temp[1]

                    false_cnt = 0
                    for ss in  temp[2]:
                        liss.append(ss)

                        if ss == 'FALSE':
                            false_cnt += 1

                    stmnt_false_cnt[stmnt_idx] += false_cnt

                    if len(l) != 0:
                        s = deepcopy(l[-1])

                stmnt_idx += 1

        all_false = False
        for val in stmnt_false_cnt:
            if val == len(lis):
                all_false = True

        if all_false and liss != []:
            liss = ['BROKEN']

        if liss != ['BROKEN']:
            ret_liss = []
            #Remove False
            for val in liss:
                if type(val) is not str:
                    ret_liss.append(val)

            liss = ret_liss

        return (l, a, liss)

    #For removing duplicate sketches
    def __eq__(self, other):
        if type(self) != type(other):
            return False

        if len(self.statements) != len(other.statements):
            return False

        for i in range(len(self.statements)):
            if self.statements[i] != other.statements[i]:
                return False

        return True

class Act:
    def __init__(self, obj, action, obj_tp=None, rel_set={}) -> None:
        self.obj = obj
        self.action = action
        self.rel_set = rel_set
        self.obj_tp = obj_tp
    def pretty_str(self, indent=0, debug=False) ->String:
        res = ''

        obj_to_print = ''
        action_to_print = ''
        rel_set_to_print= ''
        if self.obj == None:
            obj_to_print = '?'
        else:
            obj_to_print = self.obj.pretty_str(0, debug)

        if self.action == None:
            action_to_print = '?'
        else:
            action_to_print = self.action

        if self.action == 'Place' and len(self.rel_set) == 0:
            rel_set_to_print = "[(?,?)]"
        elif self.action == 'Place':
            rel_set_to_print = rel_set_to_print + ', ['
            first = True
            for rel in self.rel_set:
                rel_tp_to_print = ''
                rel_obj_to_print = ''
                if rel[0] == None:
                    rel_tp_to_print = '?'
                else:
                    rel_tp_to_print = rel[0]

                if rel[1] == None or type(rel[1]) is str:
                    rel_obj_to_print = '?'
                else:
                    rel_obj_to_print = rel[1].id

                if first:
                    first = False
                    rel_set_to_print = rel_set_to_print + '(' + str(rel_tp_to_print) + ', ' + str(rel_obj_to_print) + ')'
                else:
                    rel_set_to_print = rel_set_to_print + ', (' + str(rel_tp_to_print) + ', ' + str(rel_obj_to_print) + ')'

            rel_set_to_print = rel_set_to_print + ']'

        if debug:
            if self.action == "Place":
                res += 'act( ' + obj_to_print + ', ' + action_to_print + rel_set_to_print + ')' " ACTING ON " + self.obj_tp + '\n'
            else:
                res += 'act( ' + obj_to_print + ', ' + action_to_print + rel_set_to_print + ')' " ACTING ON " + self.obj_tp + '\n'
        else:
            res += 'act( ' + obj_to_print + ', ' + action_to_print + rel_set_to_print + ')\n'

        return res
    def execute(self, state):
        assert (type(self.action) is str)
        global variable_map
        grabbed = False
        if self.action=="Grab":
            obj = state.find_object(self.obj.get_name())
            if obj != None:
                #Check that not already grabbed
                for rob_obj in state.robot.objects:
                    if self.obj.get_name() == rob_obj:
                        grabbed = True

                if not grabbed:
                    state.robot.add_object(state.find_object(self.obj.get_name()))
                    state.find_loc(state.robot_loc).remove_object(self.obj.get_name())
        elif self.action=="Place":
            if self.obj.get_name() in state.robot.objects:
                rel_set_to_test = []
                for i in range(len(self.rel_set)):
                    if type(self.rel_set[i][1]) is not str and self.rel_set[i][1] != None and self.rel_set[i][1].get_name() != None:
                        if self.rel_set[i][0] == "Inside" and self.rel_set[i][1].get_name().split("_")[0] == "Drawer" and not state.find_object(self.rel_set[i][1].get_name()).check_prop("Open"):
                            #print("Open Drawer first")
                            return
                        if self.rel_set[i][0] == "Inside" and self.rel_set[i][1].get_name().split("_")[0] == "Fridge" and not state.find_object(self.rel_set[i][1].get_name()).check_prop("Open"):
                            #print("Open Fridge first")
                            return
                        rel_set_to_test.append((self.rel_set[i][0], self.rel_set[i][1].get_name()))
                    elif self.rel_set[i][1] != None and self.rel_set[i][1].get_name() != None:
                        if self.rel_set[i][0] == "Inside" and self.rel_set[i][1].split("_")[0] == "Drawer" and not state.find_object(self.rel_set[i][1]).check_prop("Open"):
                            #print("Open Drawer first")
                            return
                        if self.rel_set[i][0] == "Inside" and self.rel_set[i][1].split("_")[0] == "Fridge" and not state.find_object(self.rel_set[i][1]).check_prop("Open"):
                            #print("Open Fridge first")
                            return
                        rel_set_to_test.append((self.rel_set[i][0], self.rel_set[i][1]))
                state.find_loc(state.robot_loc).add_object(state.robot.objects[self.obj.get_name()])
                state.find_loc(state.robot_loc).add_relations(state.robot.objects[self.obj.get_name()], rel_set_to_test)
                state.robot.remove_object(self.obj.get_name())
        else:
            obj = state.find_object(self.obj.get_name())
            if self.action == "Clean" and "Brush" not in state.robot.get_object_types() and self.obj.get_name() != None and self.obj.get_name().split("_")[0]=="Clothes":
                #print("Hold brush first")
                return
            if self.action == "Clean" and "Cleaning" not in state.robot.get_object_types() and self.obj.get_name() != None and self.obj.get_name().split("_")[0]=="Floor":
                #print("Hold tool first")
                return [], [], []
            if self.action == "Pour" and "Bucket" not in state.robot.get_object_types() and self.obj.get_name() != None and self.obj.get_name().split("_")[0]=="Plant":
                #print("Hold Bucket first")
                return                
            if obj != None: #If object not found in location, no action to take
                obj.take_action(self.action)
        l = [state]
        if self.obj != None and self.obj.get_name() != None and not grabbed:
            if type(self.obj.get_name()) is int or type(self.action) is int:
                assert type(self.obj.get_name()) is not int
                assert type(self.action) is not int
            a = ['act( ' + self.obj.get_name() + ', ' + self.action + ' )']
        else:
            return [], [], []

        #Setup rel set for demo
        rel_set_to_test = []
        for i in range(len(self.rel_set)):
            if type(self.rel_set[i][1]) is not str and self.rel_set[i][1] != None:
                rel_set_to_test.append((self.rel_set[i][0], self.rel_set[i][1].get_name()))
            else:
                rel_set_to_test.append((self.rel_set[i][0], self.rel_set[i][1]))
        act = Act_stmnt(self.obj.get_name(),self.action,rel_set_to_test)
        return (l,a, [act])

    def partial_execute(self, state):
        if type(self.action) is not str or self.obj == None:
            return [], [], []

        grabbed = False

        global variable_map
        if self.action=="Grab":
            obj = state.find_object(self.obj.get_name())
            if obj != None:
                # Check that not already grabbed
                for rob_obj in state.robot.objects:
                    if self.obj.get_name() == rob_obj:
                        grabbed = True

                if not grabbed:
                    state.robot.add_object(state.find_object(self.obj.get_name()))
                    state.find_loc(state.robot_loc).remove_object(self.obj.get_name())
        elif self.action=="Place":
            if self.rel_set == []:
                return

            #Check that none of rel set is none
            for rel in self.rel_set:
                if rel[0] == None or rel[1] == None:
                    return

            if self.obj.get_name() in state.robot.objects:
                rel_set_to_test = []
                for i in range(len(self.rel_set)):
                    if type(self.rel_set[i][1]) is not str and self.rel_set[i][1] != None and self.rel_set[i][1].get_name() != None:
                        if self.rel_set[i][0] == "Inside" and self.rel_set[i][1].get_name().split("_")[0] == "Drawer" and not state.find_object(self.rel_set[i][1].get_name()).check_prop("Open"):
                            #print("Open Drawer first")
                            return
                        if self.rel_set[i][0] == "Inside" and self.rel_set[i][1].get_name().split("_")[0] == "Fridge" and not state.find_object(self.rel_set[i][1].get_name()).check_prop("Open"):
                            #print("Open Fridge first")
                            return
                        rel_set_to_test.append((self.rel_set[i][0], self.rel_set[i][1].get_name()))
                    elif self.rel_set[i][1] != None and type(self.rel_set[i][1]) is not str and self.rel_set[i][1].get_name() != None:
                        if self.rel_set[i][0] == "Inside" and self.rel_set[i][1].split("_")[0] == "Drawer" and not state.find_object(self.rel_set[i][1]).check_prop("Open"):
                            #print("Open Drawer first")
                            return
                        if self.rel_set[i][0] == "Inside" and self.rel_set[i][1].split("_")[0] == "Fridge" and not state.find_object(self.rel_set[i][1]).check_prop("Open"):
                            #print("Open Fridge first")
                            return
                        rel_set_to_test.append((self.rel_set[i][0], self.rel_set[i][1]))
                state.find_loc(state.robot_loc).add_object(state.robot.objects[self.obj.get_name()])
                state.find_loc(state.robot_loc).add_relations(state.robot.objects[self.obj.get_name()], rel_set_to_test)
                state.robot.remove_object(self.obj.get_name())
        else:
            obj = state.find_object(self.obj.get_name())
            if self.action == "Clean" and "Brush" not in state.robot.get_object_types() and self.obj.get_name().split("_")[0]=="Clothes":
                #print("Hold brush first")
                return
            if self.action == "Clean" and "Cleaning Tools" not in state.robot.get_object_types() and self.obj.get_name().split("_")[0]=="Floor":
                #print("Hold tool first")
                return
            if self.action == "Pour" and "Bucket" not in state.robot.get_object_types() and self.obj.get_name().split("_")[0]=="Plant":
                #print("Hold Bucket first")
                return
            if obj != None: #If object not found in location, no action to take
                obj.take_action(self.action)
        l = [state]
        if self.obj != None and self.obj.get_name() != None and not grabbed:
            if type(self.obj.get_name()) is int or type(self.action) is int:
                assert type(self.obj.get_name()) is not int
                assert type(self.action) is not int
            a = ['act( ' + self.obj.get_name() + ', ' + self.action + ' )']
        else:
            return

        #Setup rel set for demo
        rel_set_to_test = []
        for i in range(len(self.rel_set)):
            if type(self.rel_set[i][1]) is not str and self.rel_set[i][1] != None:
                rel_set_to_test.append((self.rel_set[i][0], self.rel_set[i][1].get_name()))
            else:
                rel_set_to_test.append((self.rel_set[i][0], self.rel_set[i][1]))

        act = Act_stmnt(self.obj.get_name(),self.action,rel_set_to_test)
        return (l,a, [act])

    def nl(self):
        if self.action != "Place":
            return f"{self.action} the {self.obj_tp}", 0
        else:
            holes_present = 2
            rel_to_check = "[MASK]"
            obj_to_check = "[MASK]"

            if self.rel_set != {}:
                if self.rel_set[0][0] != None:
                    rel_to_check = self.rel_set[0][0]
                    holes_present = holes_present - 1

                if self.rel_set[0][1] != None and type(self.rel_set[0][1]) is not str:
                    obj_to_check = self.rel_set[0][1].get_name()
                    holes_present = holes_present - 1

            return f"Place the {self.obj_tp} {rel_to_check} the {obj_to_check}", holes_present

    def fill_hole(self, ctx0, ctx1, hole=None, others=None):
        s = f"Place {others[0]} [MASK] {others[1]}"
        for stmnt in ctx0:
            s = stmnt + " and " + s
        for stmnt in ctx1:
            s = s + " and " + stmnt
        return s, env_def.relations

    #For removing duplicate skteches
    def __eq__(self, other):
        if type(self) != type(other):
            return False

        if self.action != other.action:
            return False

        if self.obj_tp != other.obj_tp:
            return False

        if len(self.rel_set) != len(other.rel_set):
            return False

        if len(self.rel_set) > 0:
            for i in range(len(self.rel_set)):
                if self.rel_set[i] != other.rel_set[i]:
                    return False

        return True

class variable:
    count = 0
    def __init__(self, id) -> None:
        if id != None:
            self.id = id
        else:
            self.id = f'o_{variable.count}'
            variable.count += 1
    def pretty_str(self, indent=0, debug=False) -> String:
        res = ''
        res += self.id
        return res
    def get_name(self):
        global variable_map
        if self.id in variable_map:
            return variable_map[self.id]
        else:
            return str(self.id)

class object_set:
    count = 0
    def __init__(self) -> None:
        self.id = object_set.count
        object_set.count += 1
    def pretty_str(self, indent=0, debug=False) -> String:
        res = ''
        res += "ObjSet_"+str(self.id)
        return res

class Iterator:
    count = 0
    def __init__(self) -> None:
        self.id = Iterator.count
        Iterator.count += 1
    def pretty_str(self, indent=0, debug=False) -> String:
        res = ""
        res += "i_" + str(self.id)
        return res
    def get_name(self):
        global variable_map
        if self.pretty_str(0) in variable_map:
            return variable_map[self.pretty_str(0)]
        else:
            return str(self.id)
