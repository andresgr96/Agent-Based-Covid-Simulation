import numpy as np
import pygame

from experiments.covid import population
from experiments.covid.config import config
from simulation.agent import Agent
from simulation.swarm import Swarm
from simulation.utils import *
import experiments.covid.population

experiment = "super_death"
class Person(Agent):
    """ """

    def __init__(
            self, pos, v, person, index: int,age:int, weight:int,morbid, susceptible, infectious, recovered,dead = False, image: str = "experiments/covid/images/sus.png", countInf = 0,countState = 0,sus = pygame.image.load("experiments/covid/images/sus.png"),
        inf = pygame.image.load("experiments/covid/images/inf.png"),
        rec = pygame.image.load("experiments/covid/images/cured.png"),
        death = pygame.image.load("experiments/covid/images/dead.png"),
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
        self.death = death
        self.dead = dead
        self.inf = inf
        self.rec = rec
        self.age = age
        self.weight = weight
        self.morbid = morbid

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

    def check_death(self):
        age_prob = 0
        w_prob = 0
        mor_prob = 0
        if self.age < 20:
            age_prob = 0
        elif 29 > self.age >=20:
            age_prob = 0.002
        elif 39 > self.age >=30:
            age_prob = 0.0028
        elif 49 > self.age >=40:
            age_prob = 0.004
        elif 59 > self.age >=50:
            age_prob = 0.01
        elif 69 > self.age >=60:
            age_prob = 0.036
        elif 79 > self.age >=70:
            age_prob = 0.08
        elif self.age >=80:
            age_prob = 0.18
        if self.morbid:
            mor_prob = 0.08
        elif not self.morbid:
            mor_prob = 0
        if self.weight == "under":
            w_prob = 0.01
        elif self.weight == "normal":
            w_prob = 0
        elif self.weight == "over":
            w_prob = 0.06
        elif self.weight == "obese":
            w_prob = 0.12
        u = random.uniform(0,1)
        prob = age_prob + mor_prob + w_prob
        if prob > u:
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

        elif experiment == "super_death":
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
                if self.countInf == 300 or self.countInf == 900:
                    if self.check_death():
                        self.infectious = False
                        self.dead = True
                        self.countInf = 0
                if self.countInf > 1000:
                    self.infectious = False
                    self.recovered = True
            elif self.recovered:
                self.person.datapoints.append("R")
                # print("Recovered")
                self.image = pygame.transform.scale(self.rec, (10, 10))
                self.countInf = 0
            elif self.dead:
                self.person.datapoints.append("D")
                self.wandering = False
                self.still_house = False
                self.joining = False
                self.leaving = False
                self.stop_moving()
                self.image = pygame.transform.scale(self.death, (10, 10))
                print(self.morbid, self.weight)

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

        elif experiment == "super_lock_death":
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
                if self.countInf == 300 or self.countInf == 900:
                    if self.check_death():
                        self.infectious = False
                        self.dead = True
                        self.countInf = 0
                if self.countInf > 1000:
                    self.infectious = False
                    self.recovered = True
            elif self.recovered:
                self.person.datapoints.append("R")
                # print("Recovered")
                self.image = pygame.transform.scale(self.rec, (10, 10))
                self.countInf = 0
            elif self.dead:
                self.stop_moving()
                self.image = pygame.transform.scale(self.death, (10, 10))

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