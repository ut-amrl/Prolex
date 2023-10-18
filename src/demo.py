from tokenize import String
from copy import deepcopy
variable_map = {}
class Demo:
    def __init__(self, id) -> None:
        self.id = id
        self.statements = list()
    def add_stmnt(self, stmnt):
        # assert(isinstance(stmnt, Goto_stmnt))
        self.statements.append(stmnt)
    def pretty_str(self, indent=0) -> String:
        res = 'Demo_'+str(self.id)+":\n"
        for stmnt in self.statements:
            res += stmnt.pretty_str(indent) 
        return res
    def execute(self, state):
        l = [state]
        a = []
        s = deepcopy(state)
        for stmnt in self.statements:
            temp = stmnt.execute(s)
            l += temp[0]
            a += temp[1]
            if len(l) != 0:
                s = deepcopy(l[-1])
        return (l,a)
    def apply_holes(self):
        for stmnt in self.statements:
            stmnt.apply_holes()

    def xml_str(self,indent=0) -> String:
        res  = "<demo>\n"
        for stmnt in self.statements:
            res += stmnt.xml_str(indent+1)
        res += "</demo>"
        return res

class Goto_stmnt:
    def __init__(self,loc="?loc") -> None:
        self.loc = loc 
        self.statements = list()
    def add_stmnt(self, stmnt):
        self.statements.append(stmnt)
    def pretty_str(self, indent=0) -> String:
        res = ''
        res += 'Goto( ' + self.loc + " ):\n"
        s = ''
        for i in range(indent+1):
            s += '\t'
        for stmnt in self.statements:
            res += s + stmnt.pretty_str(indent+1) 
        return res
    def execute(self, state):
        state.update_robot_loc(self.loc)
        l = [state]
        a = ['Goto( ' + self.loc + " )"]  
        s = deepcopy(state)      
        for stmnt in self.statements:
            temp = stmnt.execute(s)
            l += temp[0]
            a += temp[1]
            if len(l) != 0:
                s = deepcopy(l[-1])
        return (l,a)
    def apply_holes(self):
        for stmnt in self.statements:
            stmnt.apply_holes()

    def xml_str(self, indent=0) -> String:
        s = ''
        for i in range(indent):
            s += '\t'
        res = s + "<goto>\n"
        for stmnt in self.statements:
            res += stmnt.xml_str(indent+1) 
        res += s + "</goto>\n"
        return res

    #For Infeasibility check
    def partial_eq(self, other):
        if type(self) != type(other):
            return False
        if self.loc != other.loc:
            return False

        return True

class Scan_stmnt:
    def __init__(self, obj_tp="?obj_type", obj_tp_hole=False) -> None:
        assert(type(obj_tp) is str)
        # assert(obj_tp in env_def.object_types)
        self.obj_tp = obj_tp

        self.obj_tp_hole = obj_tp_hole
    def pretty_str(self, indent=0) -> String:
        res = ''
        # os = Object_set()
        # res += os.pretty_str() + ' = Scan( ' + self.obj_tp + " )\n"
        if self.obj_tp == None:
            obj_print = "?"
        else:
            obj_print = self.obj_tp
        res += 'Scan( ' + obj_print + " )\n"
        return res
    def execute(self, state):
        global variable_map
        lis = state.find_loc(state.robot_loc).perform_scan(self.obj_tp)
        # variable_map[self.obj_set.pretty_str(0)] = lis
        l = []
        a = []
        return (l, a)
    def apply_holes(self):
        if self.obj_tp_hole:
            self.obj_tp = "?"

    def xml_str(self, indent=0) -> String:
        s = ''
        for i in range(indent):
            s += '\t'
        res = s + "<scan> </scan>\n"
        return res

# class Let_stmnt:
#     def __init__(self, v, v_bar, i) -> None:
#         self.v = v
#         self.v_bar = v_bar
#         self.i = i
#     def pretty_str(self, indent=0) -> String:
#         res = ''
#         res += 'Let ' + self.v + ' = ' + self.v_bar +  "[" + str(self.i) + "]\n"
#         return res
#     def execute(self, state):
#         global variable_map
#         variable_map[self.v] = list(variable_map[self.v_bar.pretty_str(0)])[self.i]
#         l = []
#         a = []
#         return (l, a)

class Bexp_stmnt:
    def __init__(self, tp, right) -> None:
        assert(tp in {'neg', 'single', 'and', 'or'})
        self.tp = tp
        self.right = right
    def pretty_str(self, indent=0) -> String:
        res = ''
        if self.tp == 'or':
            res += '(' + self.left.pretty_str(0) + ')' + ' \/ ' + '(' + self.right.pretty_str(0) + ')'
        elif self.tp == 'neg':
            res += '~' + '(' + self.right.pretty_str(0) + ')'
        elif self.tp == 'and':
            res += '(' + self.left.pretty_str(0) + ')' +  " /\ " + '(' + self.right.pretty_str(0) + ')'
        else:
            res += '(' + self.right.pretty_str(0) + ')'
        return res + "\n"
    def execute(self, state):
        l = []
        a = []
        return (l, a)

    def apply_holes(self):
        self.right.apply_holes()

    def xml_str(self, indent=0) -> String:
        s = ''
        for i in range(indent):
            s += '\t'
        res = s + "<check> </check>\n"
        return res
    

class Check_prop_pred:
    def __init__(self, obj=None, obj_prop=None, obj_tp_hole=False, obj_prop_hole=False) -> None:
        assert(type(obj_prop) is str)
        self.obj = obj
        self.obj_prop = obj_prop

        self.obj_tp_hole = obj_tp_hole
        self.obj_prop_hole = obj_prop_hole
    def pretty_str(self, indent=0) -> String:
        res = ''
        if self.obj == None:
            obj_print = '?'
        else:
            obj_print = self.obj

        if self.obj_prop == None:
            prop_print = '?'
        else:
            prop_print = self.obj_prop

        res += 'Check_prop( ' + obj_print + ', ' + prop_print + ' )'
        return res
    def execute(self, state):
        l = []
        a = []
        return (l, a)

    def apply_holes(self):
        if self.obj_tp_hole:
            self.obj = "?"

        if self.obj_prop_hole:
            self.obj_prop = "?"

    def xml_str(self, indent=0) -> String:
        s = ''
        for i in range(indent):
            s += '\t'
        res = s + "<check> </check>\n"
        return res


class Check_rel_pred:
    def __init__(self, obj1="?obj1", obj2="?obj2", rel="?rel", obj1_tp_hole=False, obj2_tp_hole=False, rel_hole=False) -> None:
        assert(type(rel) is str)
        self.obj1 = obj1
        self.obj2 = obj2
        self.rel = rel

        self.obj1_tp_hole = obj1_tp_hole
        self.obj2_tp_hole = obj2_tp_hole
        self.rel_hole = rel_hole
    def pretty_str(self, indent=0) -> String:
        res = ''
        if self.obj1 == None:
            obj1_print = '?'
        else:
            obj1_print = self.obj1

        if self.obj2 == None:
            obj2_print = "?"
        else:
            obj2_print = self.obj2

        if self.rel == None:
            rel_print = "?"
        else:
            rel_print = self.rel

        res += 'Check_rel( ' + obj1_print + ', ' + obj2_print + ', ' + rel_print + ' )'
        return res
    def execute(self, state):
        l = []
        a = []
        return (l, a)

    def apply_holes(self):
        if self.obj1_tp_hole:
            self.obj1 = "?"

        if self.obj2_tp_hole:
            self.obj2 = "?"

        if self.rel_hole:
            self.rel = "?"

    def xml_str(self, indent=0) -> String:
        s = ''
        for i in range(indent):
            s += '\t'
        res = s + "<check> </check>\n"
        return res

class Act_stmnt:
    def __init__(self, obj, action, rel_set={}) -> None:
        assert(type(action) is str)
        global variable_map
        if type(obj) is not str and obj.pretty_str()[:2] == "v_":
            self.obj = variable_map[obj]
            self.obj_name = obj.pretty_str()
        else:
            self.obj = obj
            self.obj_name = obj
        self.action = action
        self.rel_set = rel_set
    def pretty_str(self, indent=0) ->String:
        res = ''
        s = ' ['
        for rel in self.rel_set:
            s = s + '[' + rel[0] + ',' + rel[1] +'],'
        s = s[:-1] + ']'

        if len(self.rel_set) > 0:
            res += 'act( ' + self.obj_name + ', ' + self.action + ',' + s + ' )\n'
        else:
            res += 'act( ' + self.obj_name + ', ' + self.action + ' )\n'
        return res
    def execute(self, state):
        if self.action=="Grab":
            state.robot.add_object(state.find_object(self.obj))
            state.find_loc(state.robot_loc).remove_object(self.obj)
        elif self.action=="Place":
            if self.obj in state.robot.objects:
                state.find_loc(state.robot_loc).add_object(state.robot.objects[self.obj])
                state.find_loc(state.robot_loc).add_relations(state.robot.objects[self.obj], self.rel_set)
                state.robot.remove_object(self.obj)
        else:
            state.find_object(self.obj).take_action(self.action)
        l = [state]
        a = ['act( ' + self.obj + ', ' + self.action + ' )']
        return (l,a)

    def apply_holes(self):
        return

    def xml_str(self, indent=0) -> String:
        s = ''
        for i in range(indent):
            s += '\t'
        res = s + "<action> </action>\n"
        return res

    def partial_eq(self, other):
        if type(self) != type(other):
            return False
        if self.obj != other.obj:
            return False
        if self.action != other.action:
            return False

        if len(self.rel_set) != len(other.rel_set):
            return False

        for i in range(len(self.rel_set)):
            found = False
            for j in range(len(other.rel_set)):
                if self.rel_set[i][0] == other.rel_set[j][0] and self.rel_set[i][1] == other.rel_set[j][1]:
                    found = True

            if not found:
                return False

        return True

# class Object_set:
#     count = 0
#     def __init__(self) -> None:
#         self.id = Object_set.count
#         Object_set.count += 1
#     def pretty_str(self, indent=0) -> String:
#         res = ''
#         res += "ObjSet_"+str(self.id)
#         return res

class Variable:
    count = 0
    def __init__(self) -> None:
        self.id = Variable.count
        Variable.count += 1
    def pretty_str(self, indent=0) -> String:
        res = ''
        res += "v_"+str(self.id)
        return res

# class Let_stmnt:
#     def __init__(self, v, v_bar, i) -> None:
#         self.v = v
#         self.v_bar = v_bar
#         self.i = i
#     def pretty_str(self, indent=0) -> String:
#         res = ''
#         v_to_print = ''
#         v_bar_to_print = ''
#         i_to_print = ''
#         if self.v == None:
#             v_to_print = '?'
#         else:
#             v_to_print = self.v.pretty_str(0)

#         if self.v_bar == None:
#             v_bar_to_print = '?'
#         else:
#             v_bar_to_print = self.v_bar.pretty_str(0)

#         if self.i == None:
#             i_to_print = '?'
#         else:
#             i_to_print = str(self.i)

#         res += 'Let ' + v_to_print + ' = ' + v_bar_to_print +  "[" + i_to_print + "]\n"
#         return res
#     def execute(self, state):
#         global variable_map
#         variable_map[self.v] = list(variable_map[self.v_bar.pretty_str(0)])[self.i]
#         l = [] 
#         a = []
#         return (l, a)
