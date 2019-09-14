import random
import grid


class Agent:
    def __init__(self, pos, type):
        self.type = type

    def step(self):
        for neighbor in self.grid.get_neighbors(self.pos):
            if neighbor.type == self.type:
                similar += 1

        if similar < self.model.homophily:
            self.model.grid.move_to_empty(self)
        else:
            pass


class Model:
    def __init__(self, height=10, width=10, density=0.8, homophily=3):
        self.height = height
        self.width = width
        self.density = density
        self.homophily = homophily

        self.grid = grid.Grid(height, width)

        # Set up agents
        for row in range(self.grid.height):
            for cell in range(self.grid.width):
                if random.random() < self.density:
                    rdm = random.random()
                    if rdm < 0.33:
                        type = 0
                    elif rdm > 0.66:
                        type = 1
                    else:
                        type = 2

                    agent = Agent((row, cell), type)
                    self.grid.place_agent(agent, (row, cell))

            self.running = 1
