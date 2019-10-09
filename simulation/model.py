import random
import grid
import scheduler


class Agent:
    def __init__(self, pos, model, agent_type, age, destroy=False, building=False):
        # Type student (0), adult (1), or elderly (2)
        self.pos = pos
        self.type = agent_type
        self.model = model
        self.age = age
        self.destroy = destroy
        self.building = building

    def step(self):
        similar = 0
        # Iterate over the neighbors of the agent
        for neighbor in self.model.grid.get_neighbors(self.pos, rad=1):
            # neighbor = self.model.scheduler.agents.get(coordinates)
            try:
                # Check if the type of the agents is the same
                if neighbor.type == self.type:
                    similar += 1
            except AttributeError:
                pass

        # Check if one of the neighbors is a building with correct type
        within_radius = False
        for neighbor in self.model.grid.get_neighbors(self.pos, rad=2):
            try:
                if neighbor.type == self.type and neighbor.building:
                    within_radius = True
            except AttributeError:
                pass

        # If agent is unhappy move it, else it stays
        if similar < self.model.homophily or within_radius is False:
            self.model.grid.move_to_empty(self)
            self.model.moves += 1
        else:
            self.model.happy += 1

        # Increase the age of the agent by 1 each step
        self.age += 1

        # Let the agents advance to a new group
        if self.type != 2:
            if self.age % self.model.ageing == 0:
                self.type += 1
            else:
                pass

        # If the agent is too old it is removed from the simulation
        if self.type == 2 and self.age == self.model.ageing * 3:
            self.destroy = True
            self.model.deaths +=1


class Building:
    def __init__(self, pos, model, building_type, building=True):
        self.pos = pos
        self.type = building_type
        self.building = building


class Model:
    def __init__(self, height=10, width=10, density=0.8, homophily=2, ageing=3, reproduction=0.5):
        # Initial parameters
        self.height = height
        self.width = width
        self.density = density
        self.homophily = homophily
        self.ageing = ageing
        self.reproduction = reproduction

        # Define a grid and scheduler
        self.grid = grid.Grid(height, width)
        self.scheduler = scheduler.Scheduler(self)
        
        #Define values for data collection
        self.happy = 0
        self.moves = 0
        self.deaths = 0
        self.births = 0
        self.happy_plot = []
        self.moves_plot = []
        self.deaths_plot = []
        self.births_plot = []
        self.total_agents = []
        self.adult_agents = []
        self.young_agents = []
        self.elderly_agents = []

        # Set up buildings
        # FOR NOW: Just create 3 different buildings,
        # one for each type, in top left, top right, and middle under
        coord = (int(self.width * 0.2), int(self.height * 0.2))
        building = Building(coord, self, 0)
        self.grid.place_agent(coord, building)

        coord = (int(self.width * 0.2), int(self.height * 0.8))
        building = Building(coord, self, 1)
        self.grid.place_agent(coord, building)

        coord = (int(self.width * 0.6), int(self.height * 0.6))
        building = Building(coord, self, 2)
        self.grid.place_agent(coord, building)

        # Set up agents
        for row in range(self.grid.width):
            for col in range(self.grid.height):
                if random.random() < self.density and self.grid[row][col] is None:
                    rdm = random.random()
                    # Randomly make agents student (0),
                    # adults (1), or elderly (2), or add building
                    if rdm < 0.33:
                        agent_type = 0
                        agent = Agent((row, col), self, agent_type, age=random.randrange(3))
                    elif rdm > 0.66:
                        agent_type = 1
                        agent = Agent((row, col), self, agent_type, age=self.ageing + random.randrange(3))
                    else:
                        agent_type = 2
                        agent = Agent((row, col), self, agent_type, age=int(self.ageing * 2) + random.randrange(3))
                    # Add agents, place them on the grid and add them to the scheduler
                    self.grid.place_agent((row, col), agent)
                    self.scheduler.add(agent)

        self.running = True

    def step(self):
        self.happy = 0
        self.moves = 0
        self.deaths = 0
        self.births = 0
        self.scheduler.step()

        # If all the agents are happy, stop the simulation
        if self.happy == self.scheduler.get_agent_number() and self.happy != 0:
            self.running = False
