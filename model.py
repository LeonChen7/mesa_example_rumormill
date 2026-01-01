import mesa
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.discrete_space import OrthogonalVonNeumannGrid, OrthogonalMooreGrid
from agent import Person


class RumorMillModel(Model):

    def __init__(self, width=10, height=10, know_rumor_ratio=0.01, rumor_spread_chance=0.5, eight_neightborhood=False, seed=None):
        super().__init__(seed=seed)
        self.number_of_agents = width * height
        self.know_rumor_ratio = know_rumor_ratio
        self.rumor_spread_chance = rumor_spread_chance
        if eight_neightborhood:
            self.grid = OrthogonalMooreGrid((width, height), random=self.random)
        else:
            self.grid = OrthogonalVonNeumannGrid((width, height), random=self.random)

        num_initial_rumor_knowers = int(self.number_of_agents * self.know_rumor_ratio)
        colors = ["red"] * num_initial_rumor_knowers + ["blue"] * (self.number_of_agents - num_initial_rumor_knowers)
        self.random.shuffle(colors)

        


        Person.create_agents(
            self,
            self.number_of_agents,
            list(self.grid.all_cells.cells),
            rumor_spread_chance=self.rumor_spread_chance,
            color=colors,
        )

        for agent in self.agents:
            if (agent.color == "red"):
                agent.knows_rumor = True
                agent.times_heard = 1

        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Percentage_Knowing_Rumor": self.compute_percentage_knowing_rumor,
                "Times_Heard_Rumor": self.compute_average_times_heard,
                "Ratio_Knowing_Rumor": self.compute_ratio_knowing_rumor
            }
        )
        self.datacollector.collect(self)

    def step(self):
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)

    def compute_percentage_knowing_rumor(self):
        agents_knowing = sum(1 for agent in self.agents if agent.knows_rumor)
        return (agents_knowing / self.number_of_agents) * 100 if self.number_of_agents > 0 else 0

    def compute_average_times_heard(self):
        total_times_heard = sum(agent.times_heard for agent in self.agents)
        return total_times_heard / self.number_of_agents if self.number_of_agents > 0 else 0

    def compute_ratio_knowing_rumor(self):
        agents_knowing = sum(1 for agent in self.agents if agent.knows_rumor)
        return agents_knowing / self.number_of_agents if self.number_of_agents > 0 else 0