from Action import *
from Orientation import *
from Location import Location
from State import State
from Percept import Percept
from Agent import find_path_networkx, escape_plan_action


class WumpusWorld(object):
    def __init__(self, file_information=None):
        """ __init__: create a new wumpus world, randomly placing the wumpus and the gold, and multiple pits """
        self.num_actions = 0

        # Update the current state
        self.current_state = State(file_information=file_information)

        # Update current percepts
        self.current_percept = Percept()

        if Location.adjacent(self.current_state.agent_location, self.current_state.wumpus_location) or \
                (self.current_state.agent_location == self.current_state.wumpus_location):
            self.current_percept.stench = True

        for pit in self.current_state.pit_locations:
            if Location.adjacent(self.current_state.agent_location, pit):
                self.current_percept.breeze = True

        if self.current_state.gold_location.x == 1 and self.current_state.gold_location.y == 1:
            self.current_percept.glitter = True

    def initialize(self):
        """ initialize: called at the start of a new try, resets certain aspects to default """

        self.num_actions = 0
        self.current_state.initialize()
        self.current_percept.initialize()

        if Location.adjacent(self.current_state.agent_location, self.current_state.wumpus_location) or \
                (self.current_state.agent_location == self.current_state.wumpus_location):
            self.current_percept.stench = True

        for pit in self.current_state.pit_locations:
            if Location.adjacent(self.current_state.agent_location, pit):
                self.current_percept.breeze = True

        if self.current_state.gold_location.x == 1 and self.current_state.gold_location.y == 1:
            self.current_percept.glitter = True

    def get_percept(self):
        """ get_percept: return the current percept for the agent's location """
        return self.current_percept

    def get_state(self):
        """ get_percept: return the current agent's state """
        return self.current_state

    # update breeze/stench/glitter percepts by determine if pits/wumpus/gold is close
    def isPitAdjacent(self):
        for pit in self.current_state.pit_locations:
            if Location.adjacent(self.current_state.agent_location, pit):
                return True
        return False

    def isBreeze(self):
        return self.isPitAdjacent()

    def isWumpusAdjacent(self):
        if Location.adjacent(self.current_state.agent_location, self.current_state.wumpus_location) or \
                (self.current_state.agent_location == self.current_state.wumpus_location):
            return True
        else:
            return False

    def isStench(self):
        return self.isWumpusAdjacent()

    def isGlitter(self):
        if (not self.current_state.agent_has_gold) and \
                (self.current_state.agent_location == self.current_state.gold_location):
            return True
        else:
            return False

    #  killAttemptSuccessful: hasArrow && wumpusAlive && wumpusInLineOfFire
    def killAttemptSuccessful(self):
        if (self.current_state.agent_has_arrow) and (self.current_state.wumpus_alive):
            ## WumpusInLineOfFire
            if (self.current_state.agent_orientation == RIGHT) and \
                    (self.current_state.agent_location.x < self.current_state.wumpus_location.x) and \
                    (self.current_state.agent_location.y == self.current_state.wumpus_location.y):
                return True
            elif (self.current_state.agent_orientation == UP) and \
                    (self.current_state.agent_location.x == self.current_state.wumpus_location.x) and \
                    (self.current_state.agent_location.y < self.current_state.wumpus_location.y):
                return True
            elif (self.current_state.agent_orientation == LEFT) and \
                    (self.current_state.agent_location.x > self.current_state.wumpus_location.x) and \
                    (self.current_state.agent_location.y == self.current_state.wumpus_location.y):
                return True
            elif (self.current_state.agent_orientation == DOWN) and \
                    (self.current_state.agent_location.x == self.current_state.wumpus_location.x) and \
                    (self.current_state.agent_location.y > self.current_state.wumpus_location.y):
                return True
        return False

    # Apply Actions
    def execute_action(self, action):
        """ execute_action: execute the provided action, updating the agent's location and the percepts """

        # before execute_action, add location
        self.current_state.safe_locations.append(
            (self.current_state.agent_location.x, self.current_state.agent_location.y))
        # remove duplicates
        self.current_state.safe_locations = list(dict.fromkeys(self.current_state.safe_locations))

        self.num_actions += 1
        self.current_percept.bump = False
        self.current_percept.scream = False

        if self.current_state.step_in_action > -1:
            self.current_state.step_in_action += 1

        if action == GOFORWARD:
            if self.current_state.agent_orientation == RIGHT:
                if self.current_state.agent_location.x < WORLD_SIZE:
                    self.current_state.agent_location.x += 1
                else:
                    self.current_percept.bump = True
            elif self.current_state.agent_orientation == UP:
                if self.current_state.agent_location.y < WORLD_SIZE:
                    self.current_state.agent_location.y += 1
                else:
                    self.current_percept.bump = True
            elif self.current_state.agent_orientation == LEFT:
                if self.current_state.agent_location.x > 1:
                    self.current_state.agent_location.x -= 1
                else:
                    self.current_percept.bump = True
            elif self.current_state.agent_orientation == DOWN:
                if self.current_state.agent_location.y > 1:
                    self.current_state.agent_location.y -= 1
                else:
                    self.current_percept.bump = True

            # update percepts
            ## glitter
            if self.isGlitter():
                self.current_percept.glitter = True
            else:
                self.current_percept.glitter = False
            ## stench
            if self.isStench():
                self.current_percept.stench = True
            else:
                self.current_percept.stench = False
            ## breeze
            if self.isBreeze():
                self.current_percept.breeze = True
            else:
                self.current_percept.breeze = False

            # update status
            ## agent death
            if self.current_state.agent_location in self.current_state.pit_locations:  # death by pit
                self.current_state.agent_alive = False
            elif self.current_state.wumpus_alive and \
                    (self.current_state.agent_location == self.current_state.wumpus_location):  # death by wumpus
                self.current_state.agent_alive = False
            else:
                self.current_state.agent_alive = True

        if action == TURNLEFT:
            if self.current_state.agent_orientation == RIGHT:
                self.current_state.agent_orientation = UP
            elif self.current_state.agent_orientation == UP:
                self.current_state.agent_orientation = LEFT
            elif self.current_state.agent_orientation == LEFT:
                self.current_state.agent_orientation = DOWN
            elif self.current_state.agent_orientation == DOWN:
                self.current_state.agent_orientation = RIGHT

        if action == TURNRIGHT:
            if self.current_state.agent_orientation == RIGHT:
                self.current_state.agent_orientation = DOWN
            elif self.current_state.agent_orientation == UP:
                self.current_state.agent_orientation = RIGHT
            elif self.current_state.agent_orientation == LEFT:
                self.current_state.agent_orientation = UP
            elif self.current_state.agent_orientation == DOWN:
                self.current_state.agent_orientation = LEFT

        if action == GRAB:
            if not self.current_state.agent_has_gold and \
                    (self.current_state.agent_location == self.current_state.gold_location):
                self.current_state.agent_has_gold = True
                self.current_percept.glitter = False
                # once grab, make escape plan
                print("Gold Grabbed! Making Escape Plan...")
                self.current_state.escape_plan = find_path_networkx(self.current_state.safe_locations,
                                                                    self.current_state.agent_location.x,
                                                                    self.current_state.agent_location.y)
                print('Safe Locations:', self.current_state.safe_locations)
                print("Escape Route:", self.current_state.escape_plan)
                self.current_state.action_plan = escape_plan_action(self.current_state.escape_plan,
                                                                    self.current_state.agent_orientation)
                print("Action Plan:")
                ct = 1
                for a in self.current_state.action_plan:
                    print("step", ct, ":", action_dict[a])
                    ct += 1
                self.current_state.step_in_action = 0

        if action == SHOOT:
            if self.killAttemptSuccessful():
                self.current_state.wumpus_alive = False
                self.current_percept.scream = True
            if self.current_state.agent_has_arrow:
                self.current_state.agent_has_arrow = False

        if action == CLIMB:
            if self.current_state.agent_location.x == 1 and self.current_state.agent_location.y == 1:
                if not (
                        allowClimbWithoutGold == False and self.current_state.agent_has_gold == False):  # if need gold & no gold, not allowed to climb
                    self.current_state.agent_in_cave = False
                    self.current_percept.stench = False
                    self.current_percept.breeze = False
                    self.current_percept.glitter = False

    def game_over(self):
        """ game_over: return True if the game is over, False otherwise"""
        return not self.current_state.agent_in_cave or not self.current_state.agent_alive

    def get_score(self):
        """ get_score: return the score for the current state of the game """
        score = 0
        # -1 for each action
        score -= self.num_actions

        if not self.current_state.agent_has_arrow:
            # -10 for shooting the arrow (total -11 due to lost 1 for the action)
            # -1 for shooting without arrow (normal action)
            score -= 10
        if self.current_state.agent_has_gold and not self.current_state.agent_in_cave:
            # +1000 for leaving the cave with the gold
            score += 1000
        if not self.current_state.agent_alive:
            # -1000 for dying
            score -= 1000
        return score

    def print_world(self):
        """ print_world: print the current wumpus world"""

        print("World size = {}x{}".format(WORLD_SIZE, WORLD_SIZE))

        # print out the first horizontal line
        out = "+"
        for x in range(1, WORLD_SIZE + 1):
            out += "---+"
        print(out)

        for y in range(WORLD_SIZE, 0, -1):  # print starting from the 'bottom' up

            # print out the first row, containing pits + gold + wumpus
            out = "|"

            for x in range(1, WORLD_SIZE + 1):
                if self.current_state.wumpus_location == Location(x, y):
                    if self.current_state.wumpus_alive:
                        out += "W"
                    else:
                        out += "x"
                else:
                    out += " "

                if not self.current_state.agent_has_gold and self.current_state.gold_location == Location(x, y):
                    out += "G"
                else:
                    out += " "

                _has_pit = False
                for pit in self.current_state.pit_locations:
                    if pit == Location(x, y):
                        _has_pit = True
                if _has_pit:
                    out += "P"
                else:
                    out += " "

                out += "|"

            print(out)

            # print out the second row, containing the agent
            out = "|"

            for x in range(1, WORLD_SIZE + 1):
                if self.current_state.agent_alive and self.current_state.agent_location == Location(x, y):
                    if self.current_state.agent_orientation == RIGHT:
                        out += " A>|"
                    elif self.current_state.agent_orientation == UP:
                        out += " A^|"
                    elif self.current_state.agent_orientation == LEFT:
                        out += " A<|"
                    else:
                        out += " Av|"
                else:
                    out += "   |"

            print(out)
            out = "+"

            # print out the final horizontal line
            for x in range(1, WORLD_SIZE + 1):
                out += "---+"

            print(out)

        # print the current percepts for the agent's location
        print(
            "Current percept = [stench={},breeze={},glitter={},bump={},scream={},agent_location_x={},agent_location_y={}]".format(
                self.current_percept.stench,
                self.current_percept.breeze,
                self.current_percept.glitter,
                self.current_percept.bump,
                self.current_percept.scream,
                self.current_state.agent_location.x,
                self.current_state.agent_location.y))

        print("Agent has gold = {}, agent has arrow = {}".format(
            self.current_state.agent_has_gold,
            self.current_state.agent_has_arrow))

        print("Current score = {}".format(self.get_score()))
        print('------------------------------------------------------')
        print()
        print()