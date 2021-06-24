import sys
import time

import matplotlib.pyplot as plt
import pygame

from typing import Union, Tuple
from experiments.aggregation.aggregation import Aggregations
from experiments.covid.population import Population
from experiments.flocking.flock import Flock
import matplotlib.ticker as mtick


def _plot_covid(data) -> None:
    """
    Plot the data related to the covid experiment. The plot is based on the number of Susceptible,
    Infected and Recovered agents

    Args:
    ----
        data:

    """
    output_name = "experiments/covid/plots/Covid-19-SIR%s.png" % time.strftime(
        "-%m.%d.%y-%H:%M", time.localtime()
    )
    values = ['2', '3', '4', '5', '6']
    fig = plt.figure()
    plt.plot(data["S"], label="Susceptible", color=(1, 0.5, 0))  # Orange
    plt.plot(data["I"], label="Infected", color=(1, 0, 0))  # Red
    plt.plot(data["R"], label="Recovered", color=(0, 1, 0))  # Green
    # plt.plot(data["D"], label="Dead", color=(0, 0, 0))  # Black
    plt.plot(data["H"], label="Hospitalized", color="brown")  # Green
    plt.axhline(y=1.5, label="Hospital Overload", color='black', linestyle='--')
    plt.title("Covid-19 Simulation")
    plt.xlabel("Time, 1000 = 2 Weeks")
    plt.ylabel("Population")
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter())
    fig.savefig(output_name)
    plt.show()


def _plot_weight(data) -> None:
    # Get the Keys and store them in a list
    labels = []
    sizes = []

    for x, y in data.items():
        labels.append(x)
        sizes.append(y[-1])

    # Plot
    plt.pie(sizes, labels=["Underweight", "Healthy", "Overweight", "Obese"], autopct='%1.1f%%',
            explode=(0.1, 0.1, 0.1, 0.1))
    plt.title('Population Weight Hospitalization Percentage')

    plt.axis('equal')
    plt.show()


def _plot_morb(data) -> None:
    # Get the Keys and store them in a list
    labels = []
    sizes = []

    for x, y in data.items():
        labels.append(x)
        sizes.append(y[-1])

    # Plot
    plt.pie(sizes, labels=["Pre-Conditioned", "Healthy"], autopct='%1.1f%%', explode=(0.1, 0.1))
    plt.title('Population Condition Hospitalization Percentage')

    plt.axis('equal')
    plt.show()


def _plot_sex(data) -> None:
    # Get the Keys and store them in a list
    labels = []
    sizes = []
    for x, y in data.items():
        labels.append(x)
        sizes.append(y[-1])

    # Plot
    plt.pie(sizes, labels=["Male", "Female"], autopct='%1.1f%%', explode=(0.1, 0.1))
    plt.title('Population Sex Hospitalization Percentage')

    plt.axis('equal')
    plt.show()


def _plot_age(data) -> None:
    # Get the Keys and store them in a list
    labels = []
    sizes = []
    for x, y in data.items():
        labels.append(x)
        sizes.append(y[-1])

    # Plot
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', explode=(0.1, 0.1, 0.1, 0.1))
    plt.title('Population Age Hospitalization Percentage')

    plt.axis('equal')
    plt.show()


def _plot_flock() -> None:
    """Plot the data related to the flocking experiment. TODO"""
    pass


def _plot_aggregation() -> None:
    """Plot the data related to the aggregation experiment. TODO"""
    pass


"""
General simulation pipeline, suitable for all experiments 
"""


class Simulation:
    """
    This class represents the simulation of agents in a virtual space.
    """

    def __init__(
            self,
            num_agents: int,
            screen_size: Union[Tuple[int, int], int],
            swarm_type: str,
            iterations: int):
        """
        Args:
        ----
            num_agents (int):
            screen_size (Union[Tuple[int, int], int]):
            swarm_type (str):
            iterations (int):
        """
        # general settings
        self.screensize = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        self.sim_background = pygame.Color("gray21")
        self.iter = iterations
        self.swarm_type = swarm_type

        # swarm settings
        self.num_agents = num_agents
        if self.swarm_type == "flock":
            self.swarm = Flock(screen_size)

        elif self.swarm_type == "aggregation":
            self.swarm = Aggregations(screen_size)

        elif self.swarm_type == "covid":
            self.swarm = Population(screen_size)

        else:
            print("None of the possible swarms selected")
            sys.exit()

        # update
        self.to_update = pygame.sprite.Group()
        self.to_display = pygame.sprite.Group()
        self.running = True

    def plot_simulation(self) -> None:
        """Depending on the type of experiment, plots the final data accordingly"""
        if self.swarm_type == "covid":
             _plot_covid(self.swarm.points_to_plot)
            # _plot_weight(self.swarm.h_weight_plot)
            # _plot_sex(self.swarm.h_sex_plot)
            # _plot_morb(self.swarm.h_morb_plot)
            #_plot_age(self.swarm.h_age_plot)


        elif self.swarm_type == "flock":
            _plot_flock()

        elif self.swarm_type == "aggregation":
            _plot_aggregation()

    def initialize(self) -> None:
        """Initialize the swarm, specifying the number of agents to be generated"""

        # initialize a swarm type specific environment
        self.swarm.initialize(self.num_agents)

    def simulate(self) -> None:
        """Here each frame is computed and displayed"""
        self.screen.fill(self.sim_background)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.swarm.update()
        self.swarm.display(self.screen)

        pygame.display.flip()

    def run(self) -> None:
        """
        Main cycle where the initialization and the frame-by-frame computation is performed.
        The iteration con be infinite if the parameter iter was set to -1, or with a finite number of frames
        (according to iter)
        When the GUI is closed, the resulting data is plotted according to the type of the experiment.
        """
        # initialize the environment and agent/obstacle positions
        self.initialize()

        # the simulation loop, infinite until the user exists the simulation
        # finite time parameter or infinite

        if self.iter == float("inf"):

            while self.running:
                init = time.time()
                self.simulate()

            self.plot_simulation()
        else:
            for i in range(self.iter):
                self.simulate()
            self.plot_simulation()
