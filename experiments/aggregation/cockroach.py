import numpy as np
import pygame
import time
from typing import Tuple
from simulation.agent import Agent
from simulation.utils import normalize, truncate
from experiments.aggregation.config import config
from experiments.aggregation.FSM import CockroachStateMAchine

"""
Specific ant properties and helperfunctions 
"""


class Cockroach(Agent):


    def __init__(
            self, pos, v, cockroach, index: int, image: str = "experiments/aggregation/images/ant.png"
    ) -> None:

        super(Cockroach, self).__init__(
            pos,
            v,
            image,
            max_speed=config["agent"]["max_speed"],
            min_speed=config["agent"]["min_speed"],
            mass=config["agent"]["mass"],
            width=config["agent"]["width"],
            height=config["agent"]["height"],
            dT=config["agent"]["dt"],
            index=index
        )

        self.cockroach = cockroach

    def slow_down(self) -> None:
        i = 5
        while(i !=0):
            self.min_speed = i
            self.max_speed = i
            i = i-1
    def stop_moving(self) -> None:
        self.min_speed = 0
        self.max_speed = 0



    def change_state(self) -> None:
        state = CockroachStateMAchine()
        m, sd = config["probability"]["m"], config["probability"]["sd"]  # mean and standard deviation
        pjoin = np.random.normal(m, sd) + (self.neighbors()/100)
        pleave = np.random.normal(m, sd) + (self.neighbors()/100)
        u = np.random.uniform(0.0, 1.0)
        for site in self.cockroach.objects.sites:
            collide = pygame.sprite.collide_mask(self, site)
            if bool(collide) and pjoin > u:
                state.joining_start()
        if state.is_joining:
            start_time = time.time()
            elapsed_time = time.time() - start_time
            if elapsed_time >= config["joining"]["time_join"]:
                self.stop_moving()
                state.still_start
        if state.is_still:
            self.wander()
            state.leaving_start()
        if state.is_leaving:
            state.wandering_start()
        print(state.current_state)




    def update_actions(self) -> None:
        # avoid any obstacles in the environment

        state = CockroachStateMAchine()
        m, sd = config["probability"]["m"], config["probability"]["sd"] # mean and standard deviation
        pjoin = np.random.normal(m, sd) + (self.neighbors() / 100)
        pleave = np.random.normal(m, sd) + (self.neighbors() / 100)
        u = np.random.uniform(0.0, 1.0)
        joined = None
        for site in self.cockroach.objects.sites:
            collide = pygame.sprite.collide_mask(self, site)
            if bool(collide) and pjoin > u:
                start_time = time.time()
                state.joining_start()
        if state.is_joining:
            elapsed_time = (time.time() - start_time) * 1000
            print(elapsed_time)
            if elapsed_time >= config["joining"]["time_join"]:
                self.stop_moving()
                state.still_start
                joined = True
        if joined:
            print("______________________________________________________________-")
            start_time_check = time.time()
            elapsed_time_check = (time.time() - start_time_check) * 1000
            if elapsed_time_check % 0.5 == 0 and pleave > u:
                state.leaving_start()
        if state.is_leaving:
            state.wandering_start()
        for obstacle in self.cockroach.objects.obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide):
                self.avoid_obstacle()

    def neighbors(self) -> int:
        n_neighbors = 0
        neighbors = self.cockroach.find_neighbors(self, config["ant"]["radius_view"])
        for n in neighbors:
            n_neighbors += 1
        return n_neighbors

    




