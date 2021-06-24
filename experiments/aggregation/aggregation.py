
from experiments.aggregation.cockroach import Cockroach
from experiments.aggregation.config import config
from simulation.utils import *
from simulation.swarm import Swarm
import numpy as np
import pygame
from typing import Tuple
from simulation.agent import Agent
from simulation.utils import normalize, truncate

experiment = "stage3"



class Aggregations(Swarm):

    def init(self, screen_size) -> None:
        super(Swarm, self).init(screen_size)

    def initialize(self, num_agents: int) -> None:
        """
        Initialize the whole swarm, creating and adding the obstacle objects, and the agent, placing them inside of the
        screen and avoiding the obstacles.
        :param num_agents: int:

        """
        object_loc_main = config["base"]["object_location"]
        if experiment == "stage2.0":
            self.objects.add_object(file = "experiments/flocking/images/redd.png", pos = object_loc_main, scale = [800, 800], obj_type = "obstacle")
            object_loc = config["first_circle"]["object_location"]
            self.objects.add_object(
                file="experiments/aggregation/images/greyc1.png", pos=object_loc, scale=[200, 200], obj_type="site"
            )
            object_loc = config["second_circle"]["object_location"]
            self.objects.add_object(
                file="experiments/aggregation/images/greyc1.png", pos=object_loc, scale=[200, 200], obj_type="site"
            )
        elif experiment == "stage1":
            self.objects.add_object(file="experiments/flocking/images/redd.png", pos=object_loc_main, scale=[800, 800],
                                    obj_type="obstacle")
            object_loc = config["center_circle"]["object_location"]
            self.objects.add_object(
                file="experiments/aggregation/images/greyc1.png", pos=object_loc, scale=[200, 200], obj_type="site"
            )
        elif experiment == "stage2.1":
            self.objects.add_object(file="experiments/flocking/images/redd.png", pos=object_loc_main, scale=[800, 800],
                                    obj_type="obstacle")
            object_loc = config["first_circle"]["object_location"]
            self.objects.add_object(
                file="experiments/aggregation/images/greyc1.png", pos=object_loc, scale=[200, 200], obj_type="site"
            )
            object_loc = config["second_circle"]["object_location"]
            self.objects.add_object(
                file="experiments/aggregation/images/greyc2.png", pos=object_loc, scale=[225, 225], obj_type="site"
            )
        elif experiment == "stage3":
            self.objects.add_object(file="experiments/flocking/images/redd.png", pos=object_loc_main, scale=[1000, 1000],
                                    obj_type="obstacle")
            object_loc = config["first_circle"]["object_location"]
            self.objects.add_object(
                file="experiments/aggregation/images/greyc1.png", pos=object_loc, scale=[200, 200], obj_type="site"
            )
            object_loc = config["second_circle"]["object_location"]
            self.objects.add_object(
                file="experiments/aggregation/images/greyc1.png", pos=object_loc, scale=[200, 200], obj_type="site"
            )
            object_loc = config["upper_circle"]["object_location"]
            self.objects.add_object(
                file="experiments/aggregation/images/greyc1.png", pos=object_loc, scale=[200, 200], obj_type="site"
            )
            object_loc = config["lower_circle"]["object_location"]
            self.objects.add_object(
                file="experiments/aggregation/images/greyc1.png", pos=object_loc, scale=[200, 200], obj_type="site"
            )
        elif experiment == "stage3.1":
            self.objects.add_object(file="experiments/flocking/images/redd.png", pos=object_loc_main, scale=[800, 800],
                                    obj_type="obstacle")
            object_loc = config["first_circle"]["object_location"]
            self.objects.add_object(
                file="experiments/aggregation/images/greyc1.png", pos=object_loc, scale=[200, 200], obj_type="site"
            )
            object_loc = config["second_circle"]["object_location"]
            self.objects.add_object(
                file="experiments/aggregation/images/greyc1.png", pos=object_loc, scale=[200, 200], obj_type="site"
            )
            object_loc = config["upper_circle"]["object_location"]
            self.objects.add_object(
                file="experiments/aggregation/images/greyc2.png", pos=object_loc, scale=[225, 225], obj_type="site"
            )
            object_loc = config["lower_circle"]["object_location"]
            self.objects.add_object(
                file="experiments/aggregation/images/greyc2.png", pos=object_loc, scale=[225, 225], obj_type="site")


        min_x, max_x = area(object_loc_main[0], 1000)
        min_y, max_y = area(object_loc_main[1], 1000)

        # add agents to the environment
        for index, agent in enumerate(range(num_agents)):
            coordinates = generate_coordinates(self.screen)
            while (
                    coordinates[0] >= max_x
                    or coordinates[0] <= min_x
                    or coordinates[1] >= max_y
                    or coordinates[1] <= min_y
            ):
                coordinates = generate_coordinates(self.screen)

            self.add_agent(Cockroach(pos=np.array(coordinates), v=None, cockroach=self, index=index))



