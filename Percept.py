class Percept(object):
    def __init__(self):
        """ __init__: create a new percept"""
        self.stench = False
        self.breeze = False
        self.glitter = False
        self.bump = False
        self.scream = False

    def initialize(self):
        """ initialize: reset the percepts to their default value at the start of a try """
        self.stench = False
        self.breeze = False
        self.glitter = False
        self.bump = False
        self.scream = False
