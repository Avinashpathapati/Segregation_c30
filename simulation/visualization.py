import sys
import tkinter as tk
import numpy as np
from tkinter import Button, Label
from model import Model
import matplotlib
from matplotlib import pyplot as plt
from termcolor import colored, cprint

# Matplotlib test (?)
matplotlib.use("Qt5Agg")
#print(matplotlib.get_backend())


# We want to implement another window to control the simulation replay
class Controller():
    def __init__(self, master, model, all_frames):
        # Preset parameters
        btn_height, btn_width = (1, 15)
        # Initialize model
        self.model = model
        # Define the window
        self.master = master
        master.title("Control Panel")
        master.geometry("220x180")
        master.resizable(0, 0)
        # Define message
        self.message = Label(master, text="Please keep your terminal open!\nAny feedback will be printed there.")
        self.message.pack()
        ### Define buttons
        # Exit Program
        self.exit_button = Button(master, text="Exit Program", \
            command=self.exit_program, height = btn_height, width = btn_width)
        self.exit_button.pack()
        # Make Plots
        self.plots_button = Button(master, text="Make Plots", \
            command=lambda: self.make_plots(model), height = btn_height, width = btn_width)
        self.plots_button.pack()
        # Print Info
        self.legend_button = Button(master, text="Print Legend", \
            command=self.print_legend, height = btn_height, width = 15)
        self.legend_button.pack()
        # Start Replay
        self.replay_button = Button(master, text="Start Replay", \
            command=lambda: self.start_replay(model, all_frames), height = btn_height, width = btn_width)
        self.replay_button.pack()
        # Stop Replay
        self.stop_button = Button(master, text="Stop Replay", \
            command=self.stop_replay, height = btn_height, width = btn_width)
        self.stop_button.pack()

    # Kill the entire program
    def exit_program(self):
        print("[ctrl]\tShutting down\n")
        sys.exit()
    # Make plots given model information
    def make_plots(self, model):
        plot_information(model.happy_plot, 'Percentage of happy agents',  'Epochs', '% Happy', 0,1)
        plot_information(model.moves_plot, 'Moves per epoch',  'Epochs', 'No Moves', 0,max(model.moves_plot))
        plot_information(model.deaths_plot, 'Deaths per Epoch',  'Epochs', 'No Deaths', 0,max(model.deaths_plot))
        plot_information(model.births_plot, 'Births per Epoch',  'Epochs', 'No Births', 0,max(model.births_plot))
        plot_information(model.total_agents, 'Total agents',  'Epochs', 'No Agents', 0,(int(dim)*int(dim)))
        plot_information(model.adult_agents, 'Adult agents',  'Epochs', 'No Adult Agents', 0, max(model.adult_agents))
        plot_information(model.young_agents, 'Young agents',  'Epochs', 'No Young Agents', 0, max(model.young_agents))
        plot_information(model.elderly_agents, 'Elderly agents',  'Epochs', 'No Elderly Agents', 0, max(model.elderly_agents))
        plot_information(model.similar_neighbors, 'Percentage of similar neighbors',  'Epochs', 'Percentage of similar neighbors', 0, max(model.similar_neighbors))
        print("[plots]\tNew plots were generated and stored in simulation/plots/")
    # Print information describing the legend of the simulation replay
    def print_legend(self):
        prefix = "[lgnd]\t"
        student = colored("   ", 'green', 'on_green')
        adult = colored("   ", 'blue', 'on_blue')
        elderly = colored("   ", 'red', 'on_red')
        student_happy = colored(" U ", 'white', 'on_green')
        adult_happy = colored(" O ", 'white', 'on_blue')
        elderly_happy = colored(" H ", 'white', 'on_red')
        university = colored(" U ", 'white')
        office = colored(" O ", 'white')
        hospital = colored(" H ", 'white')
        black_line = colored(" | ", 'white', attrs=['reverse'])
        print(f"{prefix}{student} is a student")
        print(f"{prefix}{student_happy} is a student who's happy because of a university")
        print(f"{prefix}{adult} is an adult")
        print(f"{prefix}{adult_happy} is an adult who's happy because of an office")
        print(f"{prefix}{elderly} is an elderly")
        print(f"{prefix}{elderly_happy} is an elderly who's happy because of a hospital")
        print(f"{prefix}{university} is a university building")
        print(f"{prefix}{office} is an office building")
        print(f"{prefix}{hospital} is a hospital building")
        print(f"{prefix}{black_line} black lines indicate the area of effect of buildings")
    # Start the replay gui
    def start_replay(self, model, all_frames):
        # Initialize replay windows
        viz = Visualization(model, all_frames)
        # To print the initial state in GUI
        viz.print_text_grid()
        # Tkinter event loop to make the window visible
        viz.root.mainloop()
    # Try to stop the GUI if running, WIP
    def stop_replay(self):
        print("[error]\tThis functionality has not been implemented yet")
        print("[error]\tExit a replay by clicking the red x of its window")
        print("[error]\tIgnore the error that follows, the Start Replay button will still work!")


class Visualization():
    def __init__(self, model, all_frames):
        # Initialize model
        self.model = model
        # self.root.after(20,self.render)
        self.root = tk.Tk()
        self.root.title("Segregation Simulation Replay")
        self.root.resizable(0, 0)
        #contains all the grid states to print in GUI
        self.text_print_arr = all_frames

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

    # This code needs commenting!
    def is_valid_row_or_col(self,row_cell,col_cell):
        if row_cell < 0 or row_cell >= self.model.grid.height:
            return False
        if col_cell < 0 or col_cell >= self.model.grid.width:
            return False
        return True

    # This code needs commenting!
    def check_facility_in_neighbourhood(self,cell_row,cell_col):
        if self.is_valid_row_or_col(cell_row-1,cell_col):
            c = self.model.grid[cell_row-1][cell_col]
            if not c is None and c.building == 1:
                return 1
            if not c is None and c.building == 2:
                return 2
        if self.is_valid_row_or_col(cell_row-1,cell_col-1):
            c = self.model.grid[cell_row-1][cell_col-1]
            if not c is None and c.building == 1:
                return 1
            if not c is None and c.building == 2:
                return 2
        if self.is_valid_row_or_col(cell_row-1,cell_col+1):
            c = self.model.grid[cell_row-1][cell_col+1]
            if not c is None and c.building == 1:
                return 1
            if not c is None and c.building == 2:
                return 2
        if self.is_valid_row_or_col(cell_row,cell_col-1):
            c = self.model.grid[cell_row][cell_col-1]
            if not c is None and c.building == 1:
                return 1
            if not c is None and c.building == 2:
                return 2
        if self.is_valid_row_or_col(cell_row,cell_col+1):
            c = self.model.grid[cell_row][cell_col+1]
            if not c is None and c.building == 1:
                return 1
            if not c is None and c.building == 2:
                return 2
        if self.is_valid_row_or_col(cell_row+1,cell_col-1):
            c = self.model.grid[cell_row+1][cell_col-1]
            if not c is None and c.building == 1:
                return 1
            if not c is None and c.building == 2:
                return 2
        if self.is_valid_row_or_col(cell_row+1,cell_col+1):
            c = self.model.grid[cell_row+1][cell_col+1]
            if not c is None and c.building == 1:
                return 1
            if not c is None and c.building == 2:
                return 2
        if self.is_valid_row_or_col(cell_row+1,cell_col):
            c = self.model.grid[cell_row+1][cell_col]
            if not c is None and c.building == 1:
                return 1
            if not c is None and c.building == 2:
                return 2
        return -1

    def text_gui(self, each_text_grid_itr):
        #to print the initial state
        if each_text_grid_itr == 0:
            each_text_grid_print = self.text_print_arr[each_text_grid_itr]
            each_text_grid_row_split = each_text_grid_print.split('\n')
            for each_row in range(len(each_text_grid_row_split)):
                each_text = each_text_grid_row_split[each_row]
                for each_col in range(len(each_text)):
                    if each_text[each_col] == ' ':
                        if self.check_facility_in_neighbourhood(each_row,each_col) == 1 or self.check_facility_in_neighbourhood(each_row,each_col) == 2:
                            tk.Label(self.root,text=" ", relief=tk.SUNKEN, width=2, fg="black", borderwidth=2).grid(row=each_row,column=each_col)
                        else:
                            tk.Label(self.root,text=" ", relief=tk.RIDGE, width=2).grid(row=each_row,column=each_col)

                    elif each_text[each_col] == 'X':
                        if self.check_facility_in_neighbourhood(each_row,each_col) == 1 or self.check_facility_in_neighbourhood(each_row,each_col) == 2:
                            tk.Label(self.root,text="X", relief=tk.SUNKEN, width=2, fg="black", bg="red", borderwidth=2).grid(row=each_row,column=each_col)
                        else:
                            tk.Label(self.root,text="X", relief=tk.RIDGE, width=2, fg="red", bg="red").grid(row=each_row,column=each_col)

                    elif each_text[each_col] == '0':
                        if self.check_facility_in_neighbourhood(each_row,each_col) == 1 or self.check_facility_in_neighbourhood(each_row,each_col) == 2:
                            tk.Label(self.root,text="O", relief=tk.SUNKEN, width=2, fg="black", bg="green", borderwidth=2).grid(row=each_row,column=each_col)
                        else:
                            tk.Label(self.root,text="O", relief=tk.RIDGE, width=2, fg="green", bg="green").grid(row=each_row,column=each_col)

                    elif each_text[each_col] == '9':
                        tk.Label(self.root,text="9", relief=tk.SUNKEN, width=2, bg="black", borderwidth=2).grid(row=each_row,column=each_col)
                    else:
                        #to print the rest of the states where text_gui is called recursively until self.text_print_arr is exhausted
                        if self.check_facility_in_neighbourhood(each_row,each_col) == 1 or self.check_facility_in_neighbourhood(each_row,each_col) == 2:
                            tk.Label(self.root,text="#", relief=tk.SUNKEN, width=2, fg="black", bg="blue", borderwidth=2).grid(row=each_row,column=each_col)
                        else:
                            tk.Label(self.root,text="#", relief=tk.RIDGE, width=2, fg="blue", bg="blue").grid(row=each_row,column=each_col)

        #to print the rest of the states
        elif each_text_grid_itr < len(self.text_print_arr):
            each_text_grid_print = self.text_print_arr[each_text_grid_itr]
            each_text_grid_row_split = each_text_grid_print.split('\n')
            for each_row in range(len(each_text_grid_row_split)):
                each_text = each_text_grid_row_split[each_row]
                for each_col in range(len(each_text)):
                    if each_text[each_col] == ' ':
                        if self.check_facility_in_neighbourhood(each_row,each_col) == 1 or self.check_facility_in_neighbourhood(each_row,each_col) == 2:
                            tk.Label(self.root,text=" ", relief=tk.SOLID, width=2, fg="black", borderwidth=2).grid(row=each_row,column=each_col)
                        else:
                            tk.Label(self.root,text=" ", relief=tk.RIDGE, width=2).grid(row=each_row,column=each_col)

                    elif each_text[each_col] == 'X':
                        if self.check_facility_in_neighbourhood(each_row,each_col) == 1 or self.check_facility_in_neighbourhood(each_row,each_col) == 2:
                            tk.Label(self.root,text="X", relief=tk.SOLID, width=2, fg="black", bg="red", borderwidth=2).grid(row=each_row,column=each_col)
                        else:
                            tk.Label(self.root,text="X", relief=tk.RIDGE, width=2, fg="red", bg="red").grid(row=each_row,column=each_col)

                    elif each_text[each_col] == '0':
                        if self.check_facility_in_neighbourhood(each_row,each_col) == 1 or self.check_facility_in_neighbourhood(each_row,each_col) == 2:
                            tk.Label(self.root,text="O", relief=tk.SOLID, width=2, fg="black", bg="green", borderwidth=2).grid(row=each_row,column=each_col)
                        else:
                            tk.Label(self.root,text="O", relief=tk.RIDGE, width=2, fg="green", bg="green").grid(row=each_row,column=each_col)

                    elif each_text[each_col] == '9':
                        tk.Label(self.root,text="9", relief=tk.SOLID, width=2, bg="black", borderwidth=2, highlightcolor="orange").grid(row=each_row,column=each_col)

                    else:
                        #to print the rest of the states where text_gui is called recursively until self.text_print_arr is exhausted
                        if self.check_facility_in_neighbourhood(each_row,each_col) == 1 or self.check_facility_in_neighbourhood(each_row,each_col) == 2:
                            tk.Label(self.root,text="#", relief=tk.SOLID, width=2, fg="black", bg="blue", borderwidth=2).grid(row=each_row,column=each_col)
                        else:
                            tk.Label(self.root,text="#", relief=tk.RIDGE, width=2, fg="blue", bg="blue").grid(row=each_row,column=each_col)

            each_text_grid_itr = each_text_grid_itr + 1
            self.root.after(750, self.text_gui,each_text_grid_itr)

        elif each_text_grid_itr == len(self.text_print_arr):
            #below commented code is to automatically close the GUI at the end. Right now not required
            #self.root.after(1000, lambda: self.root.destroy())
            each_text_grid_itr = each_text_grid_itr + 1


# Generic function to generate plots using matplotlib
def plot_information(array, title, xlabel, ylabel, ymin, ymax):
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
    plt.savefig(plots_folder + title+".png", format="png")

# Construct ascii text of 2D grid to display in GUI
def store_frame(model):
    text = ""
    for y in range(model.grid.height):
        for x in range(model.grid.width):
            c = model.grid[y][x]
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
    return text


# Initialize input parameters of model
if __name__ == '__main__':
    print("[init]\tDefault parameters:")
    print("[init]\t\tepochs:\t\t100")
    print("[init]\t\theight/width:\t10")
    print("[init]\t\tdensity:\t0.8")
    print("[init]\t\thomophily:\t2")
    print("[init]\t\tageing:\t\t3")
    print("[init]\t\treproduction:\t0.5")
    print("[init]\t\tradius:\t2")
    default = input("[init]\tDo you want default parameters? [y/n]: ")
    if default == 'n':
        epochs = input("[init]\tEnter the amount of epochs (default = 100): ")
        dim = input("[init]\tEnter dimensions of the grid (default = 20): ")
        density = input("[init]\tEnter percentage of density (default = 0.66): ")
        homophily = input("[init]\tEnter number of neighbors agent requires to be happy (default = 2): ")
        ageing = input("[init]\tEnter number of epochs it takes for agent to advance to next group (default = 3): ")
        reproduction = input("[init]\tEnter percentage of reproducibility for adults (default = 0.33): ")
        radius = input("[init]\tEnter radius effect of buildings (default = 2): ")
    else:
        # Else default parameters
        #                                                         		DON'T PUSH THESE CHANGED!
        epochs, dim, density, homophily, ageing, reproduction, radius = 100, 20, 0.66, 2, 3, 0.33, 2

    model_params = {
        "height": int(dim),
        "width": int(dim),
        "density": float(density),
        "homophily": int(homophily),
        "ageing": int(ageing),
        "reproduction": float(reproduction),
        "radius": int(radius)
    }

    # Initialize
    all_frames = []
    model = Model(**model_params)
    print()

    # Run the model
    if model.running:
        for i in range(int(epochs)):
            model.step()
            print(f"[model]\tSimulating epoch {i+1}/{epochs}", end='\r')
            all_frames.append(store_frame(model))
    print("\n[model]\tSimulations complete!")

    # Open controller window
    print("\n[ctrl]\tLaunching control panel")
    controlmaster = tk.Tk()
    controlwindow = Controller(controlmaster, model, all_frames)
    controlmaster.mainloop()
