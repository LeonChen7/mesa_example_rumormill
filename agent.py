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
    """
    A person agent that can know and spread a rumor.
    """

    def __init__(self, model, cell, rumor_spread_chance=0.5, color=None):
        """
        Initialize a Person agent.

        Args:
            model: The model instance
            cell: The cell where this agent is located
            rumor_spread_chance: Probability of successfully spreading rumor (0.0-1.0)
            color: Agent's color (red if knows rumor initially, blue otherwise)
        """
        super().__init__(model)
        self.cell = cell
        self.knows_rumor = False  # Whether agent knows the rumor
        self.times_heard = 0  # Number of times agent has heard the rumor
        self.rumor_spread_chance = rumor_spread_chance
        self.color = color if color is not None else self.random.choice(["red", "blue"])


    def step(self):
        """
        Agent behavior each step: if knows rumor, tell a random neighbor.
        """
        if self.knows_rumor:
            # Get all neighbors in the cell's neighborhood (excluding self)
            neighbors = [agent for agent in self.cell.neighborhood.agents if agent != self]
            if neighbors:
                # Randomly select one neighbor to tell
                neighbor = self.random.choice(neighbors)
                # Attempt to spread rumor with probability rumor_spread_chance
                if not neighbor.knows_rumor and self.random.random() < self.rumor_spread_chance:
                    neighbor.knows_rumor = True
                # Increment times heard counter (even if already knew)
                neighbor.times_heard += 1
    

