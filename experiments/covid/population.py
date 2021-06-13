from experiments.covid.config import config
from experiments.covid.person import Person
from simulation.swarm import Swarm
from simulation.utils import *


class Population(Swarm):
    """Class that represents the Population for the Covid experiment. TODO"""

    def __init__(self, screen_size) -> None:
        super(Population, self).__init__(screen_size)
        # To do

    def initialize(self, num_agents: int, num_infected: int) -> None:
        """
        Args:
            num_agents (int):
        """
        min_x, max_x = area(0, 1000)
        min_y, max_y = area(0, 1000)

        # add agents to the environment
        for index, agent in enumerate(range(num_infected)):
            coordinates = generate_coordinates(self.screen)
            while (
                    coordinates[0] >= max_x
                    or coordinates[0] <= min_x
                    or coordinates[1] >= max_y
                    or coordinates[1] <= min_y
            ):
                coordinates = generate_coordinates(self.screen)

            self.add_agent(Person(pos=np.array(coordinates), v=None, person=self, index=index, susceptible=False, infectious=True,recovered=False))

        for index, agent in enumerate(range(num_agents)):
            coordinates = generate_coordinates(self.screen)
            while (
                    coordinates[0] >= max_x
                    or coordinates[0] <= min_x
                    or coordinates[1] >= max_y
                    or coordinates[1] <= min_y
            ):
                coordinates = generate_coordinates(self.screen)

            self.add_agent(Person(pos=np.array(coordinates), v=None, person=self, index=index, infectious = False,susceptible=True,recovered=False))

        # To Do
        # code snipet (not complete) to avoid initializing agents on obstacles
        # given some coordinates and obstacles in the environment, this repositions the agent
        '''coordinates = generate_coordinates(self.screen)'''

        '''if config["population"]["obstacles"]:  # you need to define this variable
            for obj in self.objects.obstacles:
                rel_coordinate = relative(
                    coordinates, (obj.rect[0], obj.rect[1])
                )
                try:
                    while obj.mask.get_at(rel_coordinate):
                        coordinates = generate_coordinates(self.screen)
                        rel_coordinate = relative(
                            coordinates, (obj.rect[0], obj.rect[1])
                        )
                except IndexError:'''
