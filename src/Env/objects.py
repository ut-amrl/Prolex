import exp_config
class Object():
    def __init__(self, tp, num, props=None) -> None:
        """
        :param tp: Object Type
        :param num: Version number of this object (e.g. 5th fan created)
        :param props: Optional list of properties to be set true when initialized
        """
        assert(tp in exp_config.env_def.object_types)

        #Save object type
        self.tp = tp

        #Make object name based on type and num
        self.name = tp + '_' + str(num)

        #Initialize empty list of properties
        self.props = {}

        #Get list of possible properties for this object type and initialize them to false
        #TODO: Could initialize randomly?
        defined_props = exp_config.env_def.properties[tp]
        for prop in defined_props:
            self.props[prop] = False
        if props is not None:
            for prop in props:
                self.props[prop] = True

    def __eq__(self, other):
        if other is None:
            return False

        if self.tp != other.tp:
            return False

        if self.name != other.name:
            return False

        for prop in self.props:
            found = False
            for o_prop in other.props:
                if self.props[prop] == other.props[o_prop]:
                    found = True

            if not found:
                return False

        return True

    def update_state(self, prop, val):
        """
        :param prop: Property to be updated
        :param val: True or False, decided by interpreter
        :return: None
        """
        assert(prop in exp_config.env_def.properties[self.tp])

        self.props[prop] = val

    def print(self, num_indent=0):
        #Add number of indents
        # indents = ''
        # for i in range(num_indent):
        #     indents = indents + '|\t'
        if self.defined_props[0] == 'NoProp':
            print("IsInstanceOf(\""+self.name + "\", \"" + self.tp +"\")")
        else:
            print("IsInstanceOf(\""+self.name + "\", \"" + self.tp +"\")")
        #     s = ""
            for prop in self.props:
        #         if self.props[prop] == True:
        #             s += " is " + prop + " and"
        #         else:
        #             s += " is not " + prop + " and"
        #     print(indents + self.name + s[:-4])
            
                print("HasProperty(\"" + self.name+ "\", \"" + prop + "\")")
            # print(indents + prop + ":\t" + str(self.props[prop]))

    def compare(self, obj):
        if self.name != obj.name:
            return False
        defined_props = exp_config.env_def.properties[self.tp]
        for prop in defined_props:
            if self.props[prop] != obj.props[prop]:
                return False
        return True
    
    def check_prop(self, prop):
        if prop in self.props:
            return self.props[prop]
        else:
            return False

    def take_action(self,action):
        if action=='On':
            self.props['On'] = True
        elif action=='Off':
            self.props['On'] = False
        elif action=="Fill":
            self.props['Full'] = True
        elif action=="Empty":
            self.props['Full'] = False
        elif action=="Break":
            self.props['Broken'] = True
        elif action=="Clean":
            self.props['Clean'] = True
        elif action=="Open":
            self.props['Open'] = True
        elif action=="Close":
            self.props['Open'] = False
        elif action=='Pour':
            pass
        else:
            print("Action not implemented")
