from Agent import Agent
from Probability import Probability
import random


class ProbAgent(Agent):

    def __init__(self, gridx, gridy):
        self.algo = Probability(gridx, gridy)
        self.algo.create_stench_cond_dist()
        self.algo.construct_graph()

    def process(self, percept, state, agent):
        """ PyAgent_Process_Beeline: get back to（1,1）with gold in min steps """

        stench, breeze, glitter, bump, scream = percept.stench, percept.breeze, percept.glitter, percept.bump, percept.scream
        agent_location_x, agent_location_y, agent_has_gold = state.agent_location.x, state.agent_location.y, state.agent_has_gold

        percept_str = ""
        if stench == 1:
            name = "stench" + str(agent_location_x) + str(agent_location_y)
            state.hist_stench[name] = True
            percept_str += "Stench=True,"
        else:
            name = "stench" + str(agent_location_x) + str(agent_location_y)
            state.hist_stench[name] = False
            percept_str += "Stench=False,"
        if breeze == 1:
            state.hist_breeze.append([agent_location_x, agent_location_y])
            percept_str += "Breeze=True,"
        else:
            percept_str += "Breeze=False,"
        if glitter == 1:
            percept_str += "Glitter=True,"
        else:
            percept_str += "Glitter=False,"
        if bump == 1:
            percept_str += "Bump=True,"
        else:
            percept_str += "Bump=False,"
        if scream == 1:
            percept_str += "Scream=True,"
        else:
            percept_str += "Scream=False,"

        percept_str += "Agent_location_x=" + str(agent_location_x) + ","
        percept_str += "Agent_location_y=" + str(agent_location_y)

        print("PyAgent_Process_Beeline: ")
        print("Percept: " + percept_str)
        print("Agent has gold = {}, agent has arrow = {}".format(state.agent_has_gold, state.agent_has_arrow))
        #     print(state.safe_locations)

        if glitter == 1:
            return 3
        elif agent_has_gold == True:
            if (agent_location_x == 1 and agent_location_y == 1):
                return 5
            else:
                print("Executing Escape Plan...")
                return state.action_plan[state.step_in_action]
        else:
            self.algo.predict(state.hist_stench)
            return random.choice([0, 1, 2, 4])  # remove Grab & Climb


if __name__ == '__main__':
    prob_agent = ProbAgent(4, 4)