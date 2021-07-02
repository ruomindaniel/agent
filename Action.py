# Action
GOFORWARD = 0
TURNLEFT = 1
TURNRIGHT = 2
GRAB = 3
SHOOT = 4
CLIMB = 5


# Define Parameters

PIT_PROBABILITY = 0 #PitProb - The probability that a pit will be at any given location
allowClimbWithoutGold = True # allowClimbWithoutGold
VISUALIZATION = True
WORLD_SIZE = 4 # The size of the world, which will be a square

action_dict = dict(zip(range(6),['GOFORWARD','TURNLEFT','TURNRIGHT','GRAB','SHOOT','CLIMB']))