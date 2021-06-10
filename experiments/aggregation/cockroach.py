import numpy as np
import pygame
import time
from typing import Tuple
from datetime import timedelta
from timeloop import Timeloop
from simulation.agent import Agent
from simulation.utils import normalize, truncate
from experiments.aggregation.config import config
from experiments.aggregation.FSM import CockroachStateMAchine
import schedule
import timeloop

"""
Specific ant properties and helperfunctions 
"""

class Cockroach(Agent):

    def __init__(
            self, pos, v, cockroach, index: int, image: str = "experiments/aggregation/images/ant.png",count: int = 0, wandering = True, leaving = False, joining = False, still = False
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
            index=index,
        )
        self.count = count
        self.cockroach = cockroach
        self.wandering = wandering
        self.leaving = leaving
        self.joining = joining
        self.still = still

    def check_leave(self):
        m, sd = 0.62, 0.1
        pleave = np.random.normal(m, sd) - (self.neighbors() / 100)
        u = np.random.uniform(0.1, 1.0)
        if pleave > 0.5:
            return True
        else:
            return False

    def stop_moving(self) -> None:
        self.dT = 0

    def keep_moving(self) -> None:
        self.dT = 0.2

    def update_actions(self) -> None:
        m, sd = 0.4, 0.15  # mean and standard deviation
        pjoin = np.random.normal(m, sd) + (self.neighbors() / 100)
        u = np.random.uniform(0.7, 1.0)
        for site in self.cockroach.objects.sites:
            collide = pygame.sprite.collide_mask(self, site)
            if bool(collide) and pjoin > u and self.wandering:
                self.wandering = False
                self.joining = True
                print("joining")
        if self.joining:
            self.count += 1
            print(self.count)
            if self.count > 5:
                self.joining = False
                self.count = 0
                self. still = True
        elif self.still:
            self.stop_moving()
            self.count += 1
            print("still")
            if (self.count % 1000 == 0):
                print(self.count)
                print("intento")
                if self.check_leave():
                    print("Si")
                    self.still = False
                    self.leaving = True
                    self.count = 0
                else:
                    print("no")
                    self.count = 0
        elif self.leaving:
            print(self.count)
            print("Leaving")
            self.count+=1
            self.keep_moving()
            #self.count =+1
            if self.count >150:
                self.leaving = False
                self.wandering = True
        elif self.wandering:
            self.keep_moving()
            self.count = 0
            print("wandering")

            ##obstacle avoidance
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
