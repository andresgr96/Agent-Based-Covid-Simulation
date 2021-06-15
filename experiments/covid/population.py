from experiments.covid.config import config
from experiments.covid.pacient import Pacient
from experiments.covid.person import Person
from simulation.swarm import Swarm
from simulation.utils import *
import random

experiment = "super"

class Population(Swarm):
    """Class that represents the Population for the Covid experiment. TODO"""

    def __init__(self, screen_size) -> None:
        super(Population, self).__init__(screen_size)


    def initialize(self, num_agents: int, num_infected: int) -> None:
        if experiment == "base":
            min_x, max_x = area(0, 4000)
            min_y, max_y = area(0, 4000)

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

                self.add_agent(Person(pos=np.array(coordinates), v=None, person=self, index=index, susceptible=False,
                                      infectious=True, recovered=False))

            for index, agent in enumerate(range(num_agents)):
                coordinates = generate_coordinates(self.screen)
                while (
                        coordinates[0] >= max_x
                        or coordinates[0] <= min_x
                        or coordinates[1] >= max_y
                        or coordinates[1] <= min_y
                ):
                    coordinates = generate_coordinates(self.screen)

                self.add_agent(Person(pos=np.array(coordinates), v=None, person=self, index=index, infectious=False,
                                      susceptible=True, recovered=False))

        elif experiment == "super":
        # Horizontal row upper
            self.objects.add_object(file="experiments/covid/images/square_-_black_simple.svg.png", pos=[100,100], scale=[200, 200],
                                    obj_type="site")

            self.objects.add_object(file="experiments/covid/images/square_-_black_simple.svg.png", pos=[300, 100], scale=[200, 200],
                                    obj_type="site")

            self.objects.add_object(file="experiments/covid/images/square_-_black_simple.svg.png", pos=[500, 100], scale=[200, 200],
                                    obj_type="site")

            self.objects.add_object(file="experiments/covid/images/square_-_black_simple.svg.png", pos=[700, 100], scale=[200, 200],
                                    obj_type="site")

            self.objects.add_object(file="experiments/covid/images/square_-_black_simple.svg.png", pos=[900, 100], scale=[200, 200],
                                    obj_type="site")

            # Vertical row right
            self.objects.add_object(file="experiments/covid/images/square_-_black_simple.svg.png", pos=[900, 300], scale=[200, 200],
                                    obj_type="site")

            self.objects.add_object(file="experiments/covid/images/square_-_black_simple.svg.png", pos=[900, 500], scale=[200, 200],
                                    obj_type="site")

            self.objects.add_object(file="experiments/covid/images/square_-_black_simple.svg.png", pos=[900, 700], scale=[200, 200],
                                    obj_type="site")

            self.objects.add_object(file="experiments/covid/images/square_-_black_simple.svg.png", pos=[900, 900], scale=[200, 200],
                                    obj_type="site")

            # Horizontal row lower
            self.objects.add_object(file="experiments/covid/images/square_-_black_simple.svg.png", pos=[100, 900],
                                    scale=[200, 200],
                                    obj_type="site")

            self.objects.add_object(file="experiments/covid/images/square_-_black_simple.svg.png", pos=[300, 900],
                                    scale=[200, 200],
                                    obj_type="site")

            self.objects.add_object(file="experiments/covid/images/square_-_black_simple.svg.png", pos=[500, 900],
                                    scale=[200, 200],
                                    obj_type="site")

            self.objects.add_object(file="experiments/covid/images/square_-_black_simple.svg.png", pos=[700, 900],
                                    scale=[200, 200],
                                    obj_type="site")

            # Vertical row left
            self.objects.add_object(file="experiments/covid/images/square_-_black_simple.svg.png", pos=[100, 300],
                                    scale=[200, 200],
                                    obj_type="site")

            self.objects.add_object(file="experiments/covid/images/square_-_black_simple.svg.png", pos=[100, 500],
                                    scale=[200, 200],
                                    obj_type="site")

            self.objects.add_object(file="experiments/covid/images/square_-_black_simple.svg.png", pos=[100, 700],
                                    scale=[200, 200],
                                    obj_type="site")

            # Supermarket
            self.objects.add_object(file="experiments/covid/images/square_-_black_simple.svg.png", pos=[500,500],
                                    scale=[350, 350],
                                    obj_type="site")

            self.add_agent(
            Pacient(pos=(500,500), v=None, pacient=self, index=41, infectious=True, susceptible=False,
                   recovered=False))

            '''min_x, max_x = area(0, 4000)
            min_y, max_y = area(0, 4000)'''
            rooms = [[100.0, 700.0],[100.0, 500.0],[100.0, 300.0],[700.0, 900.0],[500.0, 900.0],[300.0, 900.0],[100.0, 900.0],[900.0, 900.0],[900.0, 700.0],[900.0, 500.0],[900.0, 300.0],
                     [900.0, 100.0],[700.0, 100.0],[500.0, 100.0],[300.0, 100.0],[100.0,100.0]]
            # add agents to the environment
            # for index, agent in enumerate(range(num_infected)):
            #     '''coordinates = generate_coordinates(self.screen)
            #     while (
            #             coordinates[0] >= max_x
            #             or coordinates[0] <= min_x
            #             or coordinates[1] >= max_y
            #             or coordinates[1] <= min_y
            #     ):
            #         coordinates = generate_coordinates(self.screen)'''
            #     random_room = random.choice(rooms)
            #     random_room[0] += np.random.uniform(0, 10)
            #     random_room[1] += np.random.uniform(0, 10)
            #     self.add_agent(Person(pos=np.array(random_room), v=None, person=self, index=index, susceptible=False, infectious=True,recovered=False))

            for index, agent in enumerate(range(num_agents)):
                random_room = random.choice(rooms)
                random_room[0] += np.random.uniform(0,10)
                random_room[1] += np.random.uniform(0,10)
                self.add_agent(Person(pos=np.array(random_room), v=None, person=self, index=index, infectious = False,susceptible=True,recovered=False))





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