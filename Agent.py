import random
from Action import *
import networkx as nx
import matplotlib.pyplot as plt


def find_path_networkx(safe_locations, agent_location_x, agent_location_y):
    """networkX - finding shortest path"""

    safe_locations.append((agent_location_x, agent_location_y))
    # remove duplicates
    safe_locations = list(dict.fromkeys(safe_locations))

    g1 = nx.grid_2d_graph(4, 4, create_using=nx.DiGraph())

    cord = []
    for x in range(1, 5):
        for y in range(1, 5):
            cord.append((x, y))

    mapping = dict(zip(g1, cord))
    g1 = nx.relabel_nodes(g1, mapping)

    pos = {}
    for n in list(g1.nodes):
        name = n
        pos[name] = n

    g1.remove_nodes_from(list(set(cord) - set(safe_locations)))

    route = nx.shortest_path(g1, (agent_location_x, agent_location_y), (1, 1))

    nx.draw_networkx(g1, pos, arrows=False, node_color="grey")  # , **options)

    # highlight escape route
    nx.draw_networkx_nodes(g1, pos, nodelist=route, node_color="red")

    highlight_edges = []
    for i in range(len(route) - 1):
        highlight_edges.append((route[i], route[i + 1]))
        i += 1

    nx.draw_networkx_edges(g1,
                           pos,
                           edgelist=highlight_edges,
                           width=3,
                           #     alpha=0.5,
                           edge_color="r", )

    plt.axis([0.5, 4.5, 0.5, 4.5])
    plt.show()

    return nx.shortest_path(g1, (agent_location_x, agent_location_y), (1, 1))


def PyAgent_Process_Naive(stench, breeze, glitter, bump, scream, agent_location_x, agent_location_y):
    """ PyAgent_Process_Naive: called with new percepts after each action to return the next RANDOM action """

    percept_str = ""
    if stench == 1:
        percept_str += "Stench=True,"
    else:
        percept_str += "Stench=False,"
    if breeze == 1:
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

    print("PyAgent_Process_Naive: " + percept_str)

    return random.randint(0, 5)


# add beeline Agent
def PyAgent_Process_Beeline(percept, state):
    """ PyAgent_Process_Beeline: get back to（1,1）with gold in min steps """

    stench, breeze, glitter, bump, scream = percept.stench, percept.breeze, percept.glitter, percept.bump, percept.scream
    agent_location_x, agent_location_y, agent_has_gold = state.agent_location.x, state.agent_location.y, state.agent_has_gold

    percept_str = ""
    if stench == 1:
        percept_str += "Stench=True,"
    else:
        percept_str += "Stench=False,"
    if breeze == 1:
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
        return random.choice([0, 1, 2, 4])  # remove Grab & Climb


def PyAgent_GameOver(score):
    """ PyAgent_GameOver: called at the end of each try """
    print("PyAgent_GameOver: score = " + str(score))


def MoveDirection(current_x, current_y, next_x, next_y):
    # direction moving
    if current_x - next_x == 0:  # ^up/downv
        if current_y > next_y:  # down
            move_direction = 3  # move down
        else:
            move_direction = 1  # move up
    elif current_y - next_y == 0:  # <left / right>
        if current_x > next_x:  # down
            move_direction = 2  # move left
        else:
            move_direction = 0  # move right
    return move_direction


def TurnOrMove(move_direction, ori, action):
    if move_direction == ori:
        action.append(0)  # goforward
    else:  # turn
        # determine which direction to term
        if abs(move_direction - ori) == 2:
            action += [1, 1, 0]  # turn left, turn left <>
            ori = (ori + 2) % 4
        elif (move_direction - ori == -1) or (move_direction - ori == 3):
            action += [2, 0]  # turn right
            ori = (ori + 3) % 4
        else:  # turn left
            action += [1, 0]  # turn left
            ori = (ori + 1) % 4
    return (ori, action)


def escape_plan_action(escape_plan, agent_orientation):  # agent_location_x, agent_location_y
    """Translate escape plan into actions"""

    action = []
    ori = agent_orientation
    for i in range(len(escape_plan) - 1):
        current_x = escape_plan[i][0]
        current_y = escape_plan[i][1]
        next_x = escape_plan[i + 1][0]
        next_y = escape_plan[i + 1][1]
        i += 1

        move_direction = MoveDirection(current_x, current_y, next_x, next_y)
        ori, action = TurnOrMove(move_direction, ori, action)

    return action


def action_to_string(action):
    """ action_to_string: return a string from the given action """
    if action == GOFORWARD:
        return "GOFORWARD"
    if action == TURNRIGHT:
        return "TURNRIGHT"
    if action == TURNLEFT:
        return "TURNLEFT"
    if action == SHOOT:
        return "SHOOT"
    if action == GRAB:
        return "GRAB"
    if action == CLIMB:
        return "CLIMB"
    return "UNKNOWN ACTION"


class Agent(object):
#     @staticmethod
#     def construct():
#         """ construct: call the agent's constructor method """
#         PyAgent_Constructor()

#     @staticmethod
#     def initialize():
#         """ initialize: call the agent's initialize method """
#         PyAgent_Initialize()

    @staticmethod
    def process(percept, state, agent):
        """ process: call the agent's process method, passing to it the percepts """
        if agent == 'naive':
            return PyAgent_Process_Naive(percept.stench, percept.breeze, percept.glitter,
                                         percept.bump, percept.scream,
                                         state.agent_location.x, state.agent_location.y)
        elif agent == 'beeline':
            return PyAgent_Process_Beeline(percept, state)
        else:
            print('No other agent.')


    @staticmethod
    def game_over(score):
        """ game_over: call the agent's game over method, passing to it the final score """
        PyAgent_GameOver(score)

#     @staticmethod
#     def destructor():
#         """ deconstructor: call the agent's destructor """
#         PyAgent_Destructor()