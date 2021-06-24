import pygame

from simulation.agent import Agent
from simulation.objects import Objects
from simulation.utils import dist

"""
General swarm class that defines general swarm properties, which are common across different swarm types
"""


class Swarm(pygame.sprite.Sprite):
    """
    Base class for the swarm of agents simulation. This class will contain the total amount of agents and obstacles
    which are present in the simulation. It will also handle the update and display of each element (agent or obstacle)
    for each frame of the GUI, as it extends the base class pygame.sprite.Sprite

    Attributes:
    ----------
         dist_temp:
         agents:
         screen:
         objects:
         points_to_plot:
         datapoints:

    """

    def __init__(self, screen_size, plot: dict = {"S": [], "I": [], "R": [], "D": [], "H":[]}, h_weight: dict = {"U": [], "H": [], "O": [], "OB": []},
                 h_sex: dict = {"M": [], "F": []},
                 h_morb_d: dict = {"T": [], "F": []},
                 h_age_d: dict = {"1-25": [], "25-45": [],"45-65": [], "65+": []}) -> None:
        """
        Args:
        ----
            screen_size:
            plot: Defaults to None
        """
        super(Swarm, self).__init__()
        self.dist_temp: dict = {}
        self.agents: list = []
        self.screen = screen_size
        self.objects: Objects = Objects()
        self.points_to_plot = plot
        self.h_weight_plot = h_weight
        self.h_sex_plot = h_sex
        self.h_morb_plot = h_morb_d
        self.h_age_plot = h_age_d
        self.datapoints: list = []
        self.h_morb: list = []
        self.h_age: list = []
        self.h_sex: list = []
        self.h_weight: list = []

    def add_agent(self, agent: Agent) -> None:
        """
        Adds an agent to the pool of agents in the swarm

        Args:
        ----
            agent (Agent):

        """
        self.agents.append(agent)

    def compute_distance(self, a: Agent, b: Agent) -> float:
        """
        This method computes the euclidean distance between the considered agent and another agent of the swarm, and
        saves the result in a temporary dictionary, so the inverse (i.e. distance a-b is the same as distance b-a) does
        not need to be recomputed for this frame.

        Args:
        ----
            a (Agent): Agent in question that is performing the check of its surroundings
            b (Agent): Another of the swarm

        """
        indexes = (a.index, b.index)
        pair = (min(indexes), max(indexes))

        if pair not in self.dist_temp:
            self.dist_temp[pair] = dist(a.pos, b.pos)
        return self.dist_temp[pair]

    def find_neighbors(self, agent: Agent, radius: float) -> list:
        """
        Try to locate all the neighbors of the given agent, considering a specified radius, by computing the euclidean
        distance between the agent and any other member of the swarm

        Args:
        ----
            agent (Agent):
            radius (float):

        """
        #  Check that the each other agent is not our considered one, if the type is None or infected, and the distance
        return [neighbor for neighbor in self.agents if
                agent is not neighbor and
                neighbor.type in [None, "I"] and
                self.compute_distance(agent, neighbor) < radius]

    def remain_in_screen(self) -> None:
        """
        Before displaying everything on the next frame, check if every agent is withtin the screen (on the x or y axis).
        If it is outside of the screen, reposition it at the center.
        """
        for agent in self.agents:
            if agent.pos[0] > self.screen[0]:
                agent.pos[0] = 0.0
            if agent.pos[0] < 0:
                agent.pos[0] = float(self.screen[0])
            if agent.pos[1] < 0:
                agent.pos[1] = float(self.screen[1])
            if agent.pos[1] > self.screen[1]:
                agent.pos[1] = 0.0

    def add_point(self, lst) -> None:
        """
        Plots the number of infected and recovered

        Args:
        ----
            lst:

        """
        # Count current numbers
        values = {"S": 0, "I": 0, "R": 0, "D": 0, "H" : 0}
        for state in lst:
            values[state] += 1

        for x in values:
            self.points_to_plot[x].append(values[x])

    def add_points_new(self, lst) -> None:
        """
        Plots the number of infected and recovered

        Args:
        ----
            lst:

        """
        # Count current numbers
        values = {"U": 0, "H": 0, "O": 0, "OB": 0}
        for state in lst:
            values[state] += 1

        for x in values:
            self.h_weight_plot[x].append(values[x])

    def add_points_h_sex(self, lst) -> None:
        """
        Plots the number of infected and recovered

        Args:
        ----
            lst:

        """
        # Count current numbers
        values = {"M": 0, "F": 0}
        for state in lst:
            values[state] += 1

        for x in values:
            self.h_sex_plot[x].append(values[x])

    def add_points_age(self, lst) -> None:
        """
        Plots the number of infected and recovered

        Args:
        ----
            lst:

        """
        # Count current numbers
        values = {"1-25": 0, "25-45": 0,"45-65": 0, "65+": 0}
        for state in lst:
            values[state] += 1

        for x in values:
            self.h_age_plot[x].append(values[x])

    def add_points_h_morb(self, lst) -> None:
        """
        Plots the number of infected and recovered

        Args:
        ----
            lst:

        """
        # Count current numbers
        values = {"T": 0, "F": 0}
        for state in lst:
            values[state] += 1

        for x in values:
            self.h_morb_plot[x].append(values[x])

    def update(self) -> None:
        """
        Updates every agent, and if there is any datapoint (i.e. any change in sane-infected-recovered) add it to the
        points to be plotted. Finally, check if every agent is within the screen.
        """
        # update the movement
        self.add_points_h_sex(self.h_sex)
        self.add_points_h_morb(self.h_morb)
        self.add_points_new(self.h_weight)
        self.add_points_age(self.h_age)
        self.datapoints = []
        for agent in self.agents:
            agent.update_actions()

        if self.datapoints:
            self.add_point(self.datapoints)
        self.remain_in_screen()

    def display(self, screen: pygame.Surface) -> None:
        """
        Display the updated agents and objects for the next frame, and reset the temporary dictionary for finding
        the neighbors

        Args:
        ----
            screen (pygame.Surface):

        """
        for obstacle in self.objects.obstacles:
            obstacle.display(screen)

        for site in self.objects.sites:
            site.display(screen)

        for agent in self.agents:
            agent.update()
            agent.display(screen)
            agent.reset_frame()

        self.dist_temp = {}
