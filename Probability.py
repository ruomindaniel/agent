from pomegranate import *
from typing import List, Dict


class Probability:

    def __init__(self, xdim, ydim):
        self.xdim = xdim
        self.ydim = ydim
        self.grid_locs = self._get_grid_points()
        self.wumpusDist = DiscreteDistribution(self._get_wumpus_prob([]))
        self.model = None

    def _get_grid_points(self):
        # type: (None) -> List

        grid_x = range(1, self.xdim + 1)
        grid_y = range(1, self.ydim + 1)

        grid_locs = []
        for x in grid_x:
            for y in grid_y:
                grid_locs.append(str(x) + ',' + str(y))

        return grid_locs

    def _wumpusProb(self, location, locations, num_possible_wumpus_locs):
        if location in locations:
            return 0
        else:
            return 1. / (num_possible_wumpus_locs - len(locations))

    def _get_wumpus_prob(self, locations):
        # type: (None) -> Dict

        if len(locations) == 0:
            locations.append('1,1')

        num_possible_wumpus_locs = self.xdim * self.ydim - 1.0

        wumpus_probs = {}

        for location in self.grid_locs:
            wumpus_probs[location] = self._wumpusProb(location, locations, num_possible_wumpus_locs)

        return wumpus_probs

    def create_stench_cond_dist(self):
        list_of_cond = []
        names = []
        for x in range(1, self.xdim + 1):
            for y in range(1, self.ydim + 1):
                container = []
                name = 'stench' + str(x) + str(y)
                names.append(name)
                for u in range(1, self.xdim + 1):
                    for v in range(1, self.ydim + 1):
                        for flag in [True, False]:
                            point = list()
                            point.append(str(u)+','+str(v))
                            point.append(flag)
                            if (u == x and v == y) or (u+1 == x and v == y) or (u-1 == x and v == y) \
                                    or (u == x and v+1 == y) or (u == x and v-1 == y):
                                if flag:
                                    point.append(1)
                                else:
                                    point.append(0)
                            else:
                                if flag:
                                    point.append(0)
                                else:
                                    point.append(1)
                            container.append(point)
                # print(ConditionalProbabilityTable(container, [self.wumpusDist]).__dir__)
                list_of_cond.append(ConditionalProbabilityTable(container, [self.wumpusDist]))

        return names, list_of_cond

    def construct_graph(self):
        wumpus_node = Node(self.wumpusDist, 'wumpus')
        names, list_of_cond = self.create_stench_cond_dist()

        stench_nodes = []
        for i in range(len(names)):
            stench_nodes.append(Node(list_of_cond[i], names[i]))
        wumpus_model = BayesianNetwork('WumpusCPD')
        wumpus_model.add_states(wumpus_node)

        for i in range(len(stench_nodes)):
            wumpus_model.add_state(stench_nodes[i])

        for i in range(len(stench_nodes)):
            wumpus_model.add_edge(wumpus_node, stench_nodes[i])

        wumpus_model.bake()

        self.model = wumpus_model

    def predict(self, observations):
        if observations is None:
            observations = {'stench11': False, 'stench42': True, 'stench33': True}
        print(self.model.predict_proba(observations)[0].parameters)


if __name__ == '__main__':
    p = Probability(4, 4)
    # print(p.wumpusDist)
    names, list_of_cond = p.create_stench_cond_dist()
    p.construct_graph()
    p.predict()
