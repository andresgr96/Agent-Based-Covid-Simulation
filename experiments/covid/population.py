from experiments.covid.config import config
from experiments.covid.person import Person
from simulation.swarm import Swarm
from simulation.utils import *
import random


class Population(Swarm):
    """Class that represents the Population for the Covid experiment. TODO"""

    def __init__(self, screen_size) -> None:
        super(Population, self).__init__(screen_size)


    def initialize(self, num_agents: int, num_infected: int) -> None:
        """
        Args:
            num_agents (int):
        """
        # Wine corner
        self.objects.add_object(file="experiments/covid/images/88226-200.png", pos=[100, 150], scale=[200, 100],
                                obj_type="obstacle")

        self.objects.add_object(file="experiments/covid/images/88226-200.png", pos=[100, 350], scale=[200, 100],
                                obj_type="obstacle")

        # Left Corner
        self.objects.add_object(file="experiments/covid/images/88226-200.png", pos=[250, 250], scale=[100, 300],
                                obj_type="obstacle")

        self.objects.add_object(file="experiments/covid/images/88226-200.png", pos=[400, 250], scale=[100, 300],
                                obj_type="obstacle")

        self.objects.add_object(file="experiments/covid/images/88226-200.png", pos=[550, 250], scale=[100, 300],
                                obj_type="obstacle")

        self.objects.add_object(file="experiments/covid/images/88226-200.png", pos=[700, 250], scale=[100, 300],
                                obj_type="obstacle")

        # Cheese and stuff
        self.objects.add_object(file="experiments/covid/images/88226-200.png", pos=[900, 150], scale=[200, 100],
                                obj_type="obstacle")

        self.objects.add_object(file="experiments/covid/images/88226-200.png", pos=[900, 350], scale=[200, 100],
                                obj_type="obstacle")

        # Middle path thingy
        self.objects.add_object(file="experiments/covid/images/88226-200.png", pos=[350, 500], scale=[1000, 50],
                                obj_type="obstacle")

        # Lower and cash-out
        self.objects.add_object(file="experiments/covid/images/88226-200.png", pos=[150, 700], scale=[100, 200],
                                obj_type="obstacle")

        self.objects.add_object(file="experiments/covid/images/88226-200.png", pos=[350, 700], scale=[100, 200],
                                obj_type="obstacle")

        self.objects.add_object(file="experiments/covid/images/88226-200.png", pos=[550, 900], scale=[100, 650],
                                obj_type="obstacle")

        # Fruit and Vegi part
        self.objects.add_object(file="experiments/covid/images/88226-200.png", pos=[700, 750], scale=[100, 300],
                                obj_type="obstacle")

        self.objects.add_object(file="experiments/covid/images/88226-200.png", pos=[850, 750], scale=[100, 300],
                                obj_type="obstacle")

        # Supermarket
        self.objects.add_object(file="experiments/covid/images/square_-_black_simple.svg.png", pos=[500,500],
                                scale=[1655, 1655],
                                obj_type="obstacle")

        min_x, max_x = area(100, 3500)
        min_y, max_y = area(100, 3500)
        rooms = [[100, 700],[100, 500],[100, 300],[700, 900],[500, 900],[300, 900],[100, 900],[900, 900],[900, 700],[900, 500],[900, 300],
                 [900, 100],[700, 100],[500, 100],[300, 100],[100,100]]
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
            self.add_agent(Person(pos=np.array(coordinates), v=None, person=self, index=index, susceptible=False, infectious=True,recovered=False, incubation=False))

        for index, agent in enumerate(range(num_agents)):
            coordinates = generate_coordinates(self.screen)
            while (
                    coordinates[0] >= max_x
                    or coordinates[0] <= min_x
                    or coordinates[1] >= max_y
                    or coordinates[1] <= min_y
            ):
                coordinates = generate_coordinates(self.screen)
            print(coordinates)
            self.add_agent(Person(pos=np.array(coordinates), v=None, person=self, index=index, infectious = False,susceptible=True,recovered=False, incubation=False))
