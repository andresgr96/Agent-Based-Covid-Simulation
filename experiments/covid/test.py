min_x, max_x = area(0, 4000)
            min_y, max_y = area(0, 4000)

            # add agents to the environment
            for index, agent in enumerate(range(num_infected)):
                coordinates = generate_coordinates(self.screen)
                while (
                        coordinates[0] >= max_x
                        or coordinates[0] <= min_x
                        or coordinates[1] >= max_y
                        or coordinates[1] <= min_y
                ):
                    coordinates = generate_coordinates(self.screen)

                self.add_agent(Person(pos=np.array(coordinates), v=None, person=self, index=index, susceptible=False, infectious=True,recovered=False))

            for index, agent in enumerate(range(num_agents)):
                coordinates = generate_coordinates(self.screen)
                while (
                        coordinates[0] >= max_x
                        or coordinates[0] <= min_x
                        or coordinates[1] >= max_y
                        or coordinates[1] <= min_y
                ):
                    coordinates = generate_coordinates(self.screen)

                self.add_agent(Person(pos=np.array(coordinates), v=None, person=self, index=index, infectious = False,susceptible=True,recovered=False))