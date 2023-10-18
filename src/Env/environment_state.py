class Environment():
    def __init__(self, locations, robot, init_robot_loc) -> None:
        """

        :param locations: Dictionary of locations contained within the environment
        :param robot: Robot that exists in environment
        :param init_robot_loc: Initial location of robot (specified by a location name)
        """
        assert(init_robot_loc in locations)

        #Save Locations
        self.locations = locations

        #Save Robot
        self.robot = robot

        #Initialize Robot location
        self.robot_loc = init_robot_loc


    def __eq__(self, other):
        for locs in self.locations:
            found = False
            for olocs in other.locations:
                if self.locations[locs] == other.locations[olocs]:
                    found = True

            if not found:
                return False

        if self.robot != other.robot:
            return False

        if self.robot_loc != other.robot_loc:
            return False

        return True

    def update_robot_loc(self, location_name):
        """
        Change update robots current location to the specified location
        :param location_name: Name of location that robot is in now
        :return: None
        """

        if location_name in self.locations:
            self.robot_loc = location_name

    def print(self):
        # print("Environment: ")

        # print('|\t Locations:')

        # for loc in self.locations:
        #     self.locations[loc].print(num_indent=2)

        # print('|\t Robot:')
        # self.robot.print(num_indent=2)
        # print('|\t|\tLocation:')
        # print('|\t|\t|\t' + self.robot_loc)
        # global prt 
        # prt = []
        for loc in self.locations:
            self.locations[loc].print(num_indent=0)
        # prt.sort(reverse=True)
        # for stmnt in prt:
        #     print(stmnt)        
    
    def current_state(self):
        return (self.locations, self.robot, self.robot_loc)
    
    def compare(self, env):
        loc = env.locations
        rbt = env.robot
        r_loc = env.robot_loc
        if self.robot_loc != r_loc:
            return False
        if len(self.robot.objects) != len(rbt.objects):
            return False
        if len(self.locations) != len(loc):
            return False
        for r in self.robot.objects:
            if r not in rbt.objects or not self.robot.objects[r].compare(rbt.objects[r]):
                return False
        for l in self.locations:
            if not self.locations[l].compare(loc[l]):
                return False
        return True
    
    def find_object(self, obj_name):
        loc = self.robot_loc
        for obj in self.locations[loc].objects:
            if obj == obj_name:
                return self.locations[loc].objects[obj]
        for obj in self.robot.objects:
            if obj == obj_name:
                return self.robot.objects[obj]
        return None

    def check_rel(self, rel_name):
        loc = self.robot_loc
        for rel in self.locations[loc].relations:
            if rel == rel_name:
                return True
        return False

    def find_loc(self, l):
        for loc in self.locations:
            if loc==l:
                return self.locations[loc]