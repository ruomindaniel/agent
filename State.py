import random
from Location import Location
from Orientation import LEFT, RIGHT
from Action import WORLD_SIZE, PIT_PROBABILITY


class State(object):
    """ State: holds the information on the current state of the game """

    def __init__(self, file_information):
        """ __init__: create a new state for the wumpus world, setting locations for wumpus, pits, and gold """

        # setup randomly for wumpus, gold and pits
        self.wumpus_location = self._get_wumpus_location()
        self.gold_location = self._get_gold_location()
        self.pit_locations = self._get_pit_locations()

        # setup initial state for agent
        self.agent_location = Location(1, 1)
        self.agent_orientation = RIGHT
        self.agent_alive = True
        self.agent_has_arrow = True
        self.agent_has_gold = False
        self.agent_in_cave = True
        self.wumpus_alive = True
        self.safe_locations = []  # track safe squares
        self.escape_plan = []
        self.action_plan = []
        self.step_in_action = -1
        self.hist_stench = dict()
        self.hist_breeze = dict()

    def initialize(self):
        """ initialize: called at the start of a new try, to reset game aspects back to default """
        self.agent_location = Location(1, 1)
        self.agent_orientation = RIGHT
        self.agent_alive = True
        self.agent_has_arrow = True
        self.agent_has_gold = False
        self.agent_in_cave = True
        self.wumpus_alive = True

    def _get_gold_location(self):
        """ _get_gold_location: return a random location not (1,1) for the gold's location """
        x, y = self._get_random_location()
        return Location(x, y)

    def _get_wumpus_location(self):
        """ _get_wumpus_location: return a random location, not (1,1) for the wumpus's location """
        x, y = self._get_random_location()
        return Location(x, y)

    @staticmethod
    def _get_random_location():
        """ _get_random_location: return a random location that is not the (1,1) square """
        x = 1
        y = 1

        while (x == 1) and (y == 1):
            x = random.randint(1, WORLD_SIZE)
            y = random.randint(1, WORLD_SIZE)

        return x, y

    @staticmethod
    def _get_pit_locations():
        """ _get_pit_locations: returns an array of pit locations, randomly selected based on a probability """
        locations = []
        for x in range(1, WORLD_SIZE + 1):
            for y in range(1, WORLD_SIZE + 1):
                if (x != 1) or (y != 1):
                    # Using the PIT_PROBABILITY, randomly determine if a pit will be at this location
                    if (random.randint(0, 1000 - 1)) < (PIT_PROBABILITY * 1000):
                        locations.append(Location(x, y))
        return locations
