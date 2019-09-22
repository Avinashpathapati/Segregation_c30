from collections import OrderedDict


class Scheduler():
    def __init__(self, model):
        # Initialize scheduler, store agents in an OrderedDict
        self.model = model
        self.steps = 0
        self.agents = OrderedDict()

    # Add agent to OrderedDict
    def add(self, agent):
        self.agents[agent.pos] = agent

    # Add agent to OrderedDict
    def remove(self, agent):
        del self.agents[agent.pos]

    # Return number of agents in the OrderedDict
    def get_agent_number(self):
        return len(self.agents)

    def step(self):
        # Iterate over all the agents
        for pos, agent in self.agents.items():
            # Steps are not used yet
            self.steps += 1
            agent.step()
