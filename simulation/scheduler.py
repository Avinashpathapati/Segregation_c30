import random
import model
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

    # Remove agent to OrderedDict
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
        
        print("BEFORE ALTERATIONS ")
        print("Number of happy agents: ", self.model.happy)
        print("Number of unhappy agents: ", len(self.agents) - self.model.happy)
        print("Number agents: ", len(self.agents))
        print("Number of student agents: ", sum(agent.type == 0 for agent in self.agents.values()))
        print("Number of adults agents: ", sum(agent.type == 1 for agent in self.agents.values()))
        print("Number of elderly agents: ", sum(agent.type == 2 for agent in self.agents.values()))
        
        
        #Add plotting information:        
        self.model.happy_plot.append(float((self.model.happy)/len(self.agents)))
        self.model.moves_plot.append(self.model.moves)
        self.model.deaths_plot.append(self.model.deaths)
        self.model.total_agents.append(len(self.agents))
        self.model.adult_agents.append((sum(agent.type == 1 for agent in self.agents.values())))
        self.model.young_agents.append((sum(agent.type == 0 for agent in self.agents.values())))
        self.model.elderly_agents.append((sum(agent.type == 2 for agent in self.agents.values())))
        
        # Let adults reproduce with a certain percentage
        # NOTE: Rather not have this in this step function, but cannot mutate
        # dictionary while iterating over it (if we put this function in Agent class)
        counter = 0
        for i in range(sum(agent.type == 1 for agent in self.agents.values())):
            if random.random() <= self.model.reproduction:
                counter += 1
                # Create agents, place them on the grid and add them to the scheduler
                agent = model.Agent((None, None), self.model, agent_type=0, age=0)
                self.model.grid.place_agent_on_empty(agent)
                self.add(agent)
        
        #Add the number of births to the model for this epoch 
        self.model.births_plot.append(counter)    

        # Remove agents that are too old from grid
        agents_removed = {pos: agent for pos, agent in self.agents.items() if agent.destroy is True}
        for pos, agent in agents_removed.items():
            self.model.grid.remove_agent(agent)

        # Remove agents that are too old from the agents dictionary
        self.agents = {pos: agent for pos, agent in self.agents.items() if agent.destroy is False}
        
        # Print summary of numbers of agents in the agent groups as well as number of new agents
        print("AFTER ALTERATIONS ")
        print("Number of happy agents: ", self.model.happy)
        print("Number of unhappy agents: ", len(self.agents) - self.model.happy)
        print("Number agents: ", len(self.agents))
        print("Number of student agents: ", sum(agent.type == 0 for agent in self.agents.values()))
        print("Number of adults agents: ", sum(agent.type == 1 for agent in self.agents.values()))
        print("Number of elderly agents: ", sum(agent.type == 2 for agent in self.agents.values()))
        print("Number of new agents: ", counter)

        if not self.agents:
            self.model.running = False
