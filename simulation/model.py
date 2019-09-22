import random
import grid
import scheduler


class Agent:
    def __init__(self, pos, model, agent_type):
        # Type student (0), adult (1), or elderly (2)
        self.pos = pos
        self.type = agent_type
        self.model = model

    def step(self):
        similar = 0
        # Iterate over the neighbors of the agent
        for coordinates in self.model.grid.get_neighbors(self.pos):
            neighbor = self.model.scheduler.agents.get(coordinates)
            try:
                # Check if the type of the agents is the same
                if neighbor.type == self.type:
                    similar += 1
            except AttributeError:
                pass

        # If agent is unhappy move it, else it stays
        if similar < self.model.homophily:
            self.model.grid.move_to_empty(self)
        else:
            self.model.happy += 1


class Model:
    def __init__(self, height=10, width=10, density=0.8, homophily=2):
        # Initial parameters
        self.height = height
        self.width = width
        self.density = density
        self.homophily = homophily

        # Define a grid and scheduler
        self.grid = grid.Grid(height, width)
        self.scheduler = scheduler.Scheduler(self)
        self.happy = 0

        # Set up agents
        for row in range(self.grid.height):
            for cell in range(self.grid.width):
                if random.random() < self.density:
                    rdm = random.random()
                    # Randomly make agents student (0),
                    # adults (1), or elderly (2)
                    # if rdm < 0.33:
                    #     agent_type = 0
                    # elif rdm > 0.66:
                    #     agent_type = 1
                    # else:
                    #     agent_type = 2

                    if rdm < 0.5:
                        agent_type = 0
                    else:
                        agent_type = 1

                    # Add agents, place them on the grid and add them to the scheduler
                    agent = Agent((row, cell), self, agent_type)
                    self.grid.place_agent((row, cell), agent)
                    self.scheduler.add(agent)

        self.running = True

    def step(self):
        self.happy = 0
        self.scheduler.step()

        # If all the agents are happy, stop the simulation
        if self.happy == self.scheduler.get_agent_number():
            self.running = False
