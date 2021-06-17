import numpy as np
import pygame

from experiments.covid import population
from experiments.covid.config import config
from simulation.agent import Agent
from simulation.swarm import Swarm
from simulation.utils import *
import experiments.covid.population

experiment = "super_lock"
class Person(Agent):
    """ """

    def __init__(
            self, pos, v, person, index: int, susceptible, infectious, recovered, image: str = "experiments/covid/images/sus.png", countInf = 0,countState = 0,sus = pygame.image.load("experiments/covid/images/sus.png"),
        inf = pygame.image.load("experiments/covid/images/inf.png"),
        rec = pygame.image.load("experiments/covid/images/cured.png"),
        wandering_first = False,
        wandering_sec=False,
        still_house = True,
        still_super=False,
        leaving = False,
        joining = False,
        wandering = False

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
        self.countInf = countInf
        self.countState = countState
        self.susceptible = susceptible
        self.infectious = infectious
        self.recovered = recovered
        self.sus = sus
        self.inf = inf
        self.rec = rec
        self.wandering = wandering
        self.wandering_first = wandering_first
        self.wandering_sec = wandering_sec
        self.leaving = leaving
        self.joining = joining
        self.still_house = still_house
        self.still_super = still_super


    def check_leave_house(self):
        pleave = 0.2
        u = np.random.uniform(0, 1.0)
        if pleave > u:
            return True
        else:
            return False

    def check_infected(self):
        pinf = 0.5
        u = np.random.uniform(0, 1.0)
        if pinf > u:
            return True
        else:
            return False


    def check_mask(self):
        pinf = 0.8
        u = np.random.uniform(0, 1.0)
        if pinf > u:
            return True
        else:
            return False

    def neighbors(self) -> int:
        n_neighbors = 0
        neighbors = self.person.find_neighbors(self, config["person"]["radius_house"])
        for n in neighbors:
            if n.still_house:
                n_neighbors += 1
        print(n_neighbors)
        return n_neighbors


    def stop_moving(self) -> None:
        self.dT = 0

    def keep_moving(self) -> None:
        self.dT = 0.2

    def in_site_super(self):
        coord = self.pos
        if  (360 < coord[0] < 640 and 640 > coord[1] > 360):
            return True
        else:
            return False

    def inf_neighbors(self):
        neighbors = self.person.find_neighbors(self, config["person"]["radius_view"])
        for n in neighbors:
            if n.infectious:
                return True
            else:
                return False


    def update_actions(self) -> None:
        if experiment == "base":
            if self.susceptible:
                self.person.datapoints.append("S")
               #print("Susceptible")
                self.image = pygame.transform.scale(self.sus, (10, 10))
                if self.inf_neighbors() and self.check_infected():
                    self.susceptible = False
                    self.infectious = True
            elif self.infectious:
                self.person.datapoints.append("I")
                self.image = pygame.transform.scale(self.inf, (10, 10))
                self.countInf += 1
                #print("Infected")
                if self.countInf > 1000:
                    self.infectious = False
                    self.recovered = True
            elif self.recovered:
                self.person.datapoints.append("R")
                #print("Recovered")
                self.image = pygame.transform.scale(self.rec, (10, 10))
                self.countInf = 0
            ##obstacle avoidance
            for obstacle in self.person.objects.obstacles:
                collide = pygame.sprite.collide_mask(self, obstacle)
                if bool(collide):
                    self.avoid_obstacle()
        elif experiment == "base_mask":
            if self.susceptible:
                self.person.datapoints.append("S")
               #print("Susceptible")
                self.image = pygame.transform.scale(self.sus, (10, 10))
                if self.inf_neighbors() and self.check_mask():
                    self.susceptible = False
                    self.infectious = True
            elif self.infectious:
                self.person.datapoints.append("I")
                self.image = pygame.transform.scale(self.inf, (10, 10))
                self.countInf += 1
                #print("Infected")
                if self.countInf > 1000:
                    self.infectious = False
                    self.recovered = True
            elif self.recovered:
                self.person.datapoints.append("R")
                #print("Recovered")
                self.image = pygame.transform.scale(self.rec, (10, 10))
                self.countInf = 0
            ##obstacle avoidance
            for obstacle in self.person.objects.obstacles:
                collide = pygame.sprite.collide_mask(self, obstacle)
                if bool(collide):
                    self.avoid_obstacle()


        elif experiment == "super":
            if self.susceptible:
                self.person.datapoints.append("S")
               #print("Susceptible")
                self.image = pygame.transform.scale(self.sus, (10, 10))
                if self.inf_neighbors() and self.check_infected():
                    self.susceptible = False
                    self.infectious = True
            elif self.infectious:
                self.person.datapoints.append("I")
                self.image = pygame.transform.scale(self.inf, (10, 10))
                self.countInf += 1
                #print("Infected")
                if self.countInf > 1000:
                    self.infectious = False
                    self.recovered = True
            elif self.recovered:
                self.person.datapoints.append("R")
                #print("Recovered")
                self.image = pygame.transform.scale(self.rec, (10, 10))
                self.countInf = 0

            ##Novement states
            pjoin = 0.8
            u = np.random.uniform(0.1, 1.0)
            for site in self.person.objects.sites:
                collide = pygame.sprite.collide_mask(self, site)
                if bool(collide) and pjoin > u and self.wandering:
                    self.wandering = False
                    self.joining = True
            if self.joining:
                self.countState += 1
                if self.countState > 100:
                    if self.in_site_super():
                        self.joining = False
                        self.countState = 0
                        self.still_house = True
                    elif self.in_site_super() != True:
                        self.joining = False
                        self.countState = 0
                        self.wandering = True
            elif self.still_house:
                self.stop_moving()
                self.countState += 1
                if (self.countState % 500 == 0):
                    if self.check_leave_house():
                        self.still_house = False
                        self.leaving = True
                        self.countState = 0
                    else:
                        self.countState = 0
            elif self.leaving:
                self.countState += 1
                self.keep_moving()
                if self.countState > 150:
                    self.leaving = False
                    self.wandering = True
            elif self.wandering:
                self.keep_moving()
                self.countState = 0


        elif experiment == "super_lock":
            if self.susceptible:
                self.person.datapoints.append("S")
                # print("Susceptible")
                self.image = pygame.transform.scale(self.sus, (10, 10))
                if self.inf_neighbors() and self.check_mask():
                    self.susceptible = False
                    self.infectious = True
            elif self.infectious:
                self.person.datapoints.append("I")
                self.image = pygame.transform.scale(self.inf, (10, 10))
                self.countInf += 1
                # print("Infected")
                if self.countInf > 1000:
                    self.infectious = False
                    self.recovered = True
            elif self.recovered:
                self.person.datapoints.append("R")
                # print("Recovered")
                self.image = pygame.transform.scale(self.rec, (10, 10))
                self.countInf = 0

            ##Novement states
            pjoin = 0.8
            u = np.random.uniform(0.1, 1.0)
            for site in self.person.objects.sites:
                collide = pygame.sprite.collide_mask(self, site)
                if bool(collide) and pjoin > u and self.wandering_first:
                    self.wandering_first = False
                    self.joining = True
            if self.joining:
                print("joining")
                self.countState += 1
                if self.countState > 100:
                    if self.in_site_super():
                        self.joining = False
                        self.countState = 0
                        self.still_house = True
                    elif self.in_site_super() != True:
                        self.joining = False
                        self.countState = 0
                        self.wandering_first = True
            elif self.still_house:
                self.stop_moving()
                self.countState += 1
                if (self.countState % 200 == 0):
                    if self.check_leave_house() and self.neighbors() > 3:
                        self.still_house = False
                        self.leaving = True
                        self.countState = 0
                    else:
                        self.countState = 0
            elif self.leaving:
                self.countState += 1
                self.keep_moving()
                if self.countState > 150:
                    self.leaving = False
                    self.wandering_first = True
            elif self.wandering_first:
                self.keep_moving()
                self.countState = 0




            ##obstacle avoidance
            for obstacle in self.person.objects.obstacles:
                collide = pygame.sprite.collide_mask(self, obstacle)
                if bool(collide):
                    self.avoid_obstacle()


        pass