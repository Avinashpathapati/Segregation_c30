import random
import sys

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
        agent.pos = pos
        self.grid[x][y] = agent
        self.empty_spots.discard(pos)

    # Place agent on empty spot
    def place_agent_on_empty(self, agent):
        pos = random.choice(sorted(self.empty_spots))
        self.place_agent(pos, agent)

    # Remove agent by the Agent object itself and add to empty_spots
    def remove_agent(self, agent):
        x, y = agent.pos
        self.grid[x][y] = None
        self.empty_spots.add(agent.pos)

    # Move agent to randomly one of the coordinates in empty_spots
    # NOTE: There has to be an empty spot or else the program fails
    def move_to_empty(self, agent):
        old_pos = agent.pos
        new_pos = random.choice(sorted(self.empty_spots))
        old_x, old_y = old_pos
        new_x, new_y = new_pos
        # Move it
        agent.pos = new_pos
        self.grid[old_x][old_y] = None
        self.grid[new_x][new_y] = agent
        self.empty_spots.discard(new_pos)
        self.empty_spots.add(old_pos)

    # Returns number of active agents on the grid
    def get_num_agents(self):
        num_none = sum([row.count(None) for row in self.grid])
        return (self.height * self.width) - num_none

    # Returns number of free spots
    def get_empty_spots(self):
        return len(self.empty_spots)
        
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
