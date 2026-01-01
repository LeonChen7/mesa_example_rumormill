"""The following code was adapted from the Rumor Mill model included in Netlogo
Model information can be found at:
https://www.netlogoweb.org/launch#https://www.netlogoweb.org/assets/modelslib/Sample%20Models/Social%20Science/Rumor%20Mill.nlogox
Accessed on: November 2, 2017
Author of NetLogo code:
    \Wilensky, U. (1999). NetLogo. http://ccl.northwestern.edu/netlogo/.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""
from mesa.discrete_space import CellAgent


class Person(CellAgent):

    def __init__(self, model, cell, color=None):
        super().__init__(model)
        self.cell = cell
        self.knows_rumor = False
        self.times_heard = 0
        self.color = color if color is not None else self.random.choice(["red", "blue"])
    

    def step(self):
        if self.knows_rumor:
            neighbors = [agent for agent in self.cell.neighborhood.agents if agent != self]
            if neighbors:
                neighbor = self.random.choice(neighbors)
                if not neighbor.knows_rumor:
                    neighbor.knows_rumor = True
                neighbor.times_heard += 1
    

