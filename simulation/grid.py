
class Grid():
    def __init__(self, height, width):
        self.height = height
        self.width = width

        self.grid = []

        # Fill 2D grid with empty grid spaces
        for x in range(self.width):
            col = []
            for y in range(self.height):
                col.append(None)
            self.grid.append(col)

    def __getitem__(self, index):
        return self.grid[index]

    def place_agent(self, agent, pos):
        x, y = pos
        self.grid[x][y] = agent
