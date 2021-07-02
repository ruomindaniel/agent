class Location(object): #Coords
    """ Location: location object that holds an x, y coordinate in the map """

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @staticmethod
    def adjacent(location1, location2):
        """ adjacent: returns true if the two locations and next to each other """

        x1 = location1.x
        x2 = location2.x
        y1 = location1.y
        y2 = location2.y

        if (x1 == x2) and (y1 == (y2 - 1)) or \
           (x1 == x2) and (y1 == (y2 + 1)) or \
           (x1 == (x2 - 1)) and (y1 == y2) or \
           (x1 == (x2 + 1)) and (y1 == y2):
            return True

        return False
