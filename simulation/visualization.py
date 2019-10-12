import sys
import tkinter as tk
from tkinter import Button
from model import Model
import matplotlib.pyplot as plt

class Controller():
    def __init__(self, master, model):
        # Initialize model
        self.model = model

        # Define the window
        self.master = master
        master.title("Simulation Control")
        master.geometry("300x500")
        master.resizable(0, 0)

        # Define buttons
        self.stop_button = Button(master, text="Stop", command=self.stop)
        self.stop_button.pack()

    def stop(self, model):
        model.running = False

class Visualization():
    def __init__(self, model):
        # Initialize model
        self.model = model
        # self.root.after(20,self.render)
        self.root = tk.Tk()
        #contains all the grid states to print in GUI
        self.text_print_arr = []

    # Construct ascii text of 2D grid to display in GUI
    def render(self):
        text = ""
        for y in range(self.model.grid.height):
            for x in range(self.model.grid.width):
                c = self.model.grid[y][x]
                if c is None:
                    text += ' '
                elif c.building:
                    text += '9'
                elif c.type == 0:
                    text += 'X'
                elif c.type == 1:
                    text += '0'
                elif c.type == 2:
                    text += '#'
                else:
                    text += '+'
            text += '\n'
        self.text_print_arr.append(text)

    #Method to print the Grid states in GUI
    def print_text_grid(self):
        #to print the initial state in GUI
        self.text_gui(0)
        #to update the same window with the rest of states
        self.root.after(1000, self.text_gui,1)
        #to destroy the window finally not required now
        #self.root.after(1000, lambda: self.root.destroy())

    def text_gui(self, each_text_grid_itr):
        #to print the initial state
        if each_text_grid_itr == 0:
            each_text_grid_print = self.text_print_arr[each_text_grid_itr]
            each_text_grid_row_split = each_text_grid_print.split('\n')
            for each_row in range(len(each_text_grid_row_split)):
                each_text = each_text_grid_row_split[each_row]
                for each_col in range(len(each_text)):
                    if each_text[each_col] == ' ':
                        tk.Label(self.root,text=" ", relief=tk.RIDGE, width=15).grid(row=each_row,column=each_col)
                    elif each_text[each_col] == 'X':
                        tk.Label(self.root,text="X", relief=tk.RIDGE, width=15, fg="red").grid(row=each_row,column=each_col)
                    elif each_text[each_col] == '0':
                        tk.Label(self.root,text="O", relief=tk.RIDGE, width=15, fg="green").grid(row=each_row,column=each_col)
                    elif each_text[each_col] == '9':
                        tk.Label(self.root,text="9", relief=tk.RIDGE, width=15, fg="black").grid(row=each_row,column=each_col)
                    else:
                        #to print the rest of the states where text_gui is called recursively until self.text_print_arr is exhausted
                        tk.Label(self.root,text="#", relief=tk.RIDGE, width=15, fg="blue").grid(row=each_row,column=each_col)

        elif each_text_grid_itr < len(self.text_print_arr):
            each_text_grid_print = self.text_print_arr[each_text_grid_itr]
            each_text_grid_row_split = each_text_grid_print.split('\n')
            for each_row in range(len(each_text_grid_row_split)):
                each_text = each_text_grid_row_split[each_row]
                for each_col in range(len(each_text)):
                    if each_text[each_col] == ' ':
                        tk.Label(self.root,text=" ", relief=tk.RIDGE, width=15).grid(row=each_row,column=each_col)
                    elif each_text[each_col] == 'X':
                        tk.Label(self.root,text="X", relief=tk.RIDGE, width=15, fg="red").grid(row=each_row,column=each_col)
                    elif each_text[each_col] == '0':
                        tk.Label(self.root,text="O", relief=tk.RIDGE, width=15, fg="green").grid(row=each_row,column=each_col)
                    elif each_text[each_col] == '9':
                        tk.Label(self.root,text="9", relief=tk.RIDGE, width=15, fg="black").grid(row=each_row,column=each_col)
                    else:
                        tk.Label(self.root,text="#", relief=tk.RIDGE, width=15, fg="blue").grid(row=each_row,column=each_col)

            each_text_grid_itr = each_text_grid_itr + 1
            self.root.after(1000, self.text_gui,each_text_grid_itr)

        elif each_text_grid_itr == len(self.text_print_arr):
            #below commented code is to automatically close the GUI at the end. Right now not required
            #self.root.after(1000, lambda: self.root.destroy())
            each_text_grid_itr = each_text_grid_itr + 1
            
    def plot_information(self, array, title, xlabel, ylabel, ymin, ymax):
        # Set and check plots folder
        import os
        plots_folder = "plots/"
        if not os.path.exists(plots_folder):
            os.makedirs(plots_folder)
        plt.figure()
        plt.suptitle(title)
        axes = plt.gca()
        axes.set_ylim([ymin,ymax])
        axes.set_xlabel(xlabel)
        axes.set_ylabel(ylabel)
        plt.plot(array)
        #plt.show(block=False)
        plt.savefig(plots_folder + title, format="svg")


# Initialize input parameters of model
if __name__ == '__main__':
    print("Default parameters:")
    print("\tepochs:\t\t100")
    print("\theight/width:\t10")
    print("\tdensity:\t0.8")
    print("\thomophily:\t2")
    print("\tageing:\t\t3")
    print("\treproduction:\t0.5")
    default = input("Do you want default parameters? [y/n]: ")
    if default == 'n':
        epochs = input("Enter the amount of epochs (default = 100): ")
        dim = input("Enter dimensions of the grid (default = 10): ")
        density = input("Enter percentage of density (default = 0.8): ")
        homophily = input("Enter number of neighbors agent requires to be happy (default = 2): ")
        ageing = input("Enter number of epochs it takes for agent to advance to next group (default = 3): ")
        reproduction = input("Enter percentage of reproducibility for adults (default = 0.5): ")
    else:
        # Else default parameters
        epochs, dim, density, homophily, ageing, reproduction = 100, 20, 0.1, 2, 20, 0.05

    model_params = {
        "height": int(dim),
        "width": int(dim),
        "density": float(density),
        "homophily": int(homophily),
        "ageing": int(ageing),
        "reproduction": float(reproduction)
    }

    # Initialize
    model = Model(**model_params)
    viz = Visualization(model)
    # controlmaster = tk.Tk()
    # controlwindow = Controller(controlmaster, model)

    # Run the model
    if model.running:
        for i in range(int(epochs)):
            model.step()
            print("Step:", i + 1)
            print('----')
            viz.render()

    print("In the simulation the places on the grid represent locations an agent can live")
    print("there are three different groups of agents, namely; students(X), adults(O) and elderly(#)")
    print("Each iteration the agents grow and if unhappy move to a random location, until they are all happy")
    print("or the simulation has run 20 epochs")

    # Save the plots    
    viz.plot_information(model.happy_plot, 'Percentage of happy agents',  'Epochs', '% Happy', 0,1)
    viz.plot_information(model.moves_plot, 'Moves per epoch',  'Epochs', 'No Moves', 0,max(model.moves_plot))
    viz.plot_information(model.deaths_plot, 'Deaths per Epoch',  'Epochs', 'No Deaths', 0,max(model.deaths_plot))
    viz.plot_information(model.births_plot, 'Births per Epoch',  'Epochs', 'No Births', 0,max(model.births_plot))
    viz.plot_information(model.total_agents, 'Total agents',  'Epochs', 'No Agents', 0,(dim*dim))
    viz.plot_information(model.adult_agents, 'Adult agents',  'Epochs', 'No Adult Agents', 0, max(model.adult_agents))
    viz.plot_information(model.young_agents, 'Young agents',  'Epochs', 'No Young Agents', 0, max(model.young_agents))
    viz.plot_information(model.elderly_agents, 'Elderly agents',  'Epochs', 'No Elderly Agents', 0, max(model.elderly_agents))

    # To print the grid states in GUI
    viz.print_text_grid()
    #below commented code is to automatically close the GUI at the end. Right now not required
    # viz.root.after(1000, lambda: viz.root.destroy())
    #tkinter event loop to make the window visible
    viz.root.mainloop()

    # # Open controller window
    # controlmaster.mainloop()
