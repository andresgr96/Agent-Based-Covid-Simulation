import numpy as np
import pygame
import time
import random

from experiments.covid.config import config
from simulation.agent import Agent
from simulation.utils import *


class Person(Agent):
    """ """

    def __init__(
            self, pos, v, person, index: int, susceptible, infectious, recovered, incubation,
            image: str = "experiments/covid/images/sus.png",
            count = 0,sus = pygame.image.load("experiments/covid/images/sus.png"),
        inf = pygame.image.load("experiments/covid/images/inf.png"),
        rec = pygame.image.load("experiments/covid/images/cured.png"),
        inc = pygame.image.load("experiments/covid/images/inc.png")

    ) -> None:
        super(Person, self).__init__(
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
        self.person = person
        self.count = count
        self.susceptible = susceptible
        self.infectious = infectious
        self.recovered = recovered
        self.incubation = incubation
        self.sus = sus
        self.inf = inf
        self.rec = rec
        self.inc = inc

    def inf_neighbors(self):
        neighbors = self.person.find_neighbors(self, config["person"]["radius_view"])
        for n in neighbors:
            if n.recovered:
                print("rec")
            if n.susceptible:
                print("sus")
            if n.incubation:
                print("inc")
            if n.infectious:
                print("inf")
            if n.infectious:
                return True
            else:
                return False



    def update_actions(self) -> None:

        if self.susceptible:
           # print("Susceptible")
            self.image = pygame.transform.scale(self.sus, (10, 10))
            if self.inf_neighbors():
                self.susceptible = False
                self.incubation = True
        elif self.incubation:
            self.image = pygame.transform.scale(self.inc, (10, 10))
            self.count += 0
            if self.count > 200:
                self.incubation = False
                self.infectious = True
        elif self.infectious:
            print(self.inf_neighbors())
            self.image = pygame.transform.scale(self.inf, (10, 10))
            self.count += 0
            #print("Infected")
            if self.count > 1000:
                self.infectious = False
                self.recovered = True
        elif self.recovered:
            #print("Recovered")
            self.image = pygame.transform.scale(self.rec, (10, 10))
            self.count = 0





        ##obstacle avoidance
        for obstacle in self.person.objects.obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide):
                self.avoid_obstacle()

        pass
