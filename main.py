from WumpusWorld import WumpusWorld
from Agent import *
from Action import *


def main(WORLD_SIZE, PIT_PROBABILITY, allowClimbWithoutGold, VISUALIZATION, agent):
    """ main: the main driver for the wumpus simulator,
        continue runs until gameover"""

    score = 0
    wumpus_world = WumpusWorld()
    #     Agent.construct()  # call the constructor on the imported agent

    wumpus_world.initialize()  # call initialize on the wumpus world, resetting for the try
    #     Agent.initialize()  # call the initialize method for the imported agent

    num_moves = 0

    print("Game starts...")
    print()

    while not wumpus_world.game_over():
        if VISUALIZATION == True:
            wumpus_world.print_world()
        percept = wumpus_world.get_percept()  # get the percepts for the current location
        state = wumpus_world.get_state()
        action = Agent.process(percept, state, agent)  # and pass the percepts to the imported agent, expecting an action

        if VISUALIZATION == True:
            print("Action = {}".format(action_to_string(action)))
            print()

        wumpus_world.execute_action(action)  # execute the action in the wumpus world
        num_moves += 1

    score = wumpus_world.get_score()  # get the final score for the world
    Agent.game_over(score)  # and pass that score to the imported agent, signaling game over

    print("Game over...")
    #     Agent.destructor()  # call the deconstructor on the imported agent for this trial is over

    return score


if __name__ == '__main__':
    main(WORLD_SIZE, PIT_PROBABILITY, allowClimbWithoutGold, VISUALIZATION, agent='beeline')
