# Design of Multi-Agents Systems
## Run instructions
To run this program navigate to the simulation folder. Then type: python visualization.py

## Design Plan
### Grid
The simulation will consist of a grid which should be able to vary in size, but is always square. This grid will hold the coordinates for all agents' locations. Each age group should be sized 30% of the nTiles, leaving 10% of the tiles empty.
### Agents
Agents need to be objects with a location and age. The age should be increased by 1 each timestep. It requires basic functions such as move() and stay(), probably more.
### GUI
At each timestep some function render() should be called which takes the grid (including all agents and their positions) and draws an image from it. All age groups should have their own color. AFAIK Python is not very good at this so we need some magic.
### Mechanics
At each timestep each agent should evaluate its current situation. If it is satisfied (let's say 3/8 neighbours are of the same age), it will not move. If it is not satisfied it has to move to a random, empty tile on the map.
