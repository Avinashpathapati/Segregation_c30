from collections import OrderedDict


class Scheduler():
    def __init__(self, model):
        self.model = model
        self.steps = 0
        self.agents = OrderedDict()

    def add(self, agent):
        self.agents[agent.pos] = agent

    def remove(self, agent):
        del self.agents[agent.pos]

    def get_agent_number(self):
        return len(self.agents)

    def step(self):
        for pos, agent in self.agents.items():
            # Steps are not used yet
            self.steps += 1
            agent.step()
