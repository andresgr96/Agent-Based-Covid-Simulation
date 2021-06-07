from experiments.aggregation.cockroach import Cockroach
from experiments.aggregation.config import config
from simulation.utils import *
from simulation.swarm import Swarm
import numpy as np

from experiments.flocking.boid import Boid
from experiments.flocking.config import config
from simulation.agent import Agent
from simulation.swarm import Swarm
from simulation.utils import area, generate_coordinates, norm

class Aggregations(Swarm):
    """ """
    def __init__(self, screen_size) -> None:
        """
        This function is the initializer of the class Aggregations.
        :param screen_size:
        """
        super(Aggregations, self).__init__(screen_size)
        self.object_loc = config["aggregations"]["outside"]

    def initialize(self, num_agents: int) -> None:
        # add agents to the environment
        for index, agent in enumerate(range(num_agents)):
            coordinates = generate_coordinates(self.screen)

            self.add_agent(Cockroach(pos=np.array(coordinates), v=None, flock=self, index=index))

        # Creating 2 Aggregation Areas
        if config["aggregation"]["sites"]:



