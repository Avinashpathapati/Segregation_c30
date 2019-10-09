import random


class Grid():
    def __init__(self, height, width):
        # Initialize grid, create empty set for the empty places
        self.height = height
        self.width = width

        self.grid = []
        self.empty_spots = set()

        # Fill 2D grid with empty grid spaces
        for x in range(self.width):
            col = []
            for y in range(self.height):
                col.append(None)
                self.empty_spots.add((x, y))
            self.grid.append(col)

    # Return specific place in the grid
    def __getitem__(self, index):
        return self.grid[index]

    # Place agent on the grid, remove from the empty_spots set
    def place_agent(self, pos, agent):
        x, y = pos
        self.grid[x][y] = agent
        self.empty_spots.discard(pos)

    # Place agent on empty spot
    def place_agent_on_empty(self, agent):
        pos = random.choice(sorted(self.empty_spots))
        self.place_agent(pos, agent)
        agent.pos = pos
        self.remove_agent_by_pos(pos, agent)

    # Remove agent from grid, and add the coordinates to empty_spots set
    def remove_agent_by_pos(self, pos, agent):
        x, y = pos
        self.grid[x][y] = None
        self.empty_spots.add(pos)

    # Remove agent by the Agent object itself and add to empty_spots
    def remove_agent(self, agent):
        x, y = agent.pos
        self.grid[x][y] = None
        self.empty_spots.add(agent.pos)

    # Move agent to randomly one of the coordinates in empty_spots
    # NOTE: There has to be an empty spot or else the program fails
    def move_to_empty(self, agent):
        pos = agent.pos
        new_pos = random.choice(sorted(self.empty_spots))
        self.place_agent(new_pos, agent)
        agent.pos = new_pos
        self.remove_agent_by_pos(pos, agent)

    # Returns number of active agents on the grid
    def num_agents(self):
        num_none = sum([row.count(None) for row in self.grid])
        return (self.height * self.width) - num_none

    # Iterate over the neighbors of specific agent, return their coordinates
    def get_neighbors(self, pos, rad):
        x, y = pos
        coordinates = []
        for neighbors_y in range(-rad, rad + 1):
            for neighbors_x in range(-rad, rad + 1):
                if neighbors_x == 0 and neighbors_y == 0:
                    continue
                if (not (0 <= neighbors_x + x < self.width) or not (0 <= neighbors_y + y < self.height)):
                    continue
                else:
                    coordinates.append(self.grid[neighbors_x + x][neighbors_y + y])

        return coordinates
