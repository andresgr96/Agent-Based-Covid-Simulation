import pygame
from scipy.stats import norm
import numpy as np


mu, sigma = 0.3, 0.15 # mean and standard deviation
s = np.random.normal(mu, sigma, 10)
print(s)


import time

# creating a time delay of 5 seconds
wandering = True
joining = False
still = False
leaving = False

def update_actions(self) -> None:
    global wandering
    global joining
    global still
    global leaving
    m, sd = 0.4, 0.15  # mean and standard deviation
    pjoin = np.random.normal(m, sd) + (self.neighbors() / 100)
    pleave = np.random.normal(m, sd) - (self.neighbors() / 100)
    u = np.random.uniform(0.1, 1.0)
    for site in self.cockroach.objects.sites:
        collide = pygame.sprite.collide_mask(self, site)
        if bool(collide) and pjoin > u and wandering:
            start_time = time.time()
            wandering = False
            joining = True
    if joining:
        elapsed_time = (time.time() - start_time) * 1000
        if elapsed_time >= 0.3:
            self.stop_moving()
            joining = False
            still = True
    if still:
        self.check_leave()
        if leaving # and wait some time:
            still = False
    if leaving:
        self.keep_moving()
        #wait some seconds
        leaving = False
        wandering = True


