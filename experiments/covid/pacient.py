import numpy as np
import pygame

from experiments.covid import population
from experiments.covid.config import config
from simulation.agent import Agent
from simulation.swarm import Swarm
from simulation.utils import *
import experiments.covid.population

experiment = "super"
class Pacient(Agent):
    """ """

    def __init__(
            self, pos, v, pacient, index: int, susceptible, infectious, recovered, image: str = "experiments/covid/images/inf.png", countInf = 0,countState = 0,sus = pygame.image.load("experiments/covid/images/sus.png"),
        inf = pygame.image.load("experiments/covid/images/inf.png"),
        rec = pygame.image.load("experiments/covid/images/cured.png"),
        wandering = False,
        still = True,
        leaving = False,
        joining = False,
        still_house = False

    ) -> None:
        super(Pacient, self).__init__(
            pos,
            v,
            image,
            max_speed=config["agent"]["max_speed"],
            min_speed=config["agent"]["min_speed"],
            mass=config["agent"]["mass"],
            width=config["agent"]["width"],
            height=config["agent"]["height"],
            dT=0,
            index=index,
        )
        self.pacient = pacient
        self.countInf = countInf
        self.countState = countState
        self.susceptible = susceptible
        self.infectious = infectious
        self.recovered = recovered
        self.sus = sus
        self.inf = inf
        self.rec = rec
        self.wandering = wandering
        self.leaving = leaving
        self.joining = joining
        self.still_house = still_house
        self.still = still

    def update_actions(self) -> None:
        if self.infectious == True:
            self.pacient.datapoints.append("I")
