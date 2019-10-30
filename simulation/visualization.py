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
    def check_facility_in_neighbourhood(self,cell_row,cell_col,radius):

        
        agent_type = self.model.grid[cell_row][cell_col]
        building_list = []

        for row_bound_iter in range(-radius, radius+1):
            for col_bound_iter in range(-radius, radius+1):
                if self.is_valid_row_or_col(cell_row+row_bound_iter,cell_col+col_bound_iter):
                    c = self.model.grid[cell_row+row_bound_iter][cell_col+col_bound_iter]
                    if not c is None and c.building:
                        building_list.append(c.type)
            
        
        return building_list

    def text_gui(self, each_text_grid_itr):
        #to print the initial state
        if each_text_grid_itr == 0:


            each_text_grid_print = self.text_print_arr[each_text_grid_itr]
            each_text_grid_row_split = each_text_grid_print.split('\n')
            self.label_arr = [[0 for x in range(model.grid.width)] for y in range(model.grid.height)] 

            for each_row in range(len(each_text_grid_row_split)):
                each_text = each_text_grid_row_split[each_row]
                for each_col in range(len(each_text)):
                    # IF EMPTY
                    if each_text[each_col] == ' ':

                        building_list = self.check_facility_in_neighbourhood(each_row,each_col,self.model.radius)
                        if  not len(building_list)== 0:
                            self.label_arr[each_row][each_col] = tk.Label(self.root,text=" ", relief=tk.SOLID, width=2, fg="black", bg="white", borderwidth=2)
                            self.label_arr[each_row][each_col].grid(row=each_row,column=each_col)
                        else:
                           self.label_arr[each_row][each_col] =  tk.Label(self.root,text=" ", relief=tk.RIDGE, bg="white",width=2)
                           self.label_arr[each_row][each_col].grid(row=each_row,column=each_col)


                    # IF STUDENT
                    elif each_text[each_col] == 'S':

                        building_list = self.check_facility_in_neighbourhood(each_row,each_col,self.model.radius)

                        if 0 in building_list:
                            self.label_arr[each_row][each_col] = tk.Label(self.root,text="U", relief=tk.SOLID, width=2, fg="white", bg="green", borderwidth=2)
                            self.label_arr[each_row][each_col].grid(row=each_row,column=each_col)
                        elif not len(building_list)== 0:
                            self.label_arr[each_row][each_col] = tk.Label(self.root,text="", relief=tk.SOLID, width=2, fg="white",bg="green",borderwidth=2)
                            self.label_arr[each_row][each_col].grid(row=each_row,column=each_col)
                        else:
                            self.label_arr[each_row][each_col]  = tk.Label(self.root,text="", relief=tk.RIDGE, width=2, bg="green")
                            self.label_arr[each_row][each_col].grid(row=each_row,column=each_col)


                    
                    # IF ADULT
                    elif each_text[each_col] == 'A':

                        building_list = self.check_facility_in_neighbourhood(each_row,each_col,self.model.radius)

                        if 1 in building_list:
                            self.label_arr[each_row][each_col]  = tk.Label(self.root,text="O", relief=tk.SOLID, width=2, fg="white", bg="blue", borderwidth=2)
                            self.label_arr[each_row][each_col].grid(row=each_row,column=each_col)
                        elif not len(building_list)== 0:
                            self.label_arr[each_row][each_col]  = tk.Label(self.root,text="", relief=tk.SOLID, width=2, fg="white",bg="blue",borderwidth=2)
                            self.label_arr[each_row][each_col].grid(row=each_row,column=each_col)
                        else:
                            self.label_arr[each_row][each_col]  = tk.Label(self.root,text="", relief=tk.RIDGE, width=2, bg="blue")
                            self.label_arr[each_row][each_col].grid(row=each_row,column=each_col)
                        
                    # IF ELDERLY
                    elif each_text[each_col] == 'E':

                        building_list = self.check_facility_in_neighbourhood(each_row,each_col,self.model.radius)

                        if 2 in building_list:
                            self.label_arr[each_row][each_col]  = tk.Label(self.root,text="H", relief=tk.SOLID, width=2, fg="white", bg="red", borderwidth=2)
                            self.label_arr[each_row][each_col].grid(row=each_row,column=each_col)
                        elif not len(building_list)== 0:
                            self.label_arr[each_row][each_col]  = tk.Label(self.root,text="", relief=tk.SOLID, width=2, fg="white",bg="red",borderwidth=2)
                            self.label_arr[each_row][each_col].grid(row=each_row,column=each_col)
                        else:
                            self.label_arr[each_row][each_col]  = tk.Label(self.root,text="", relief=tk.RIDGE, width=2, bg="red")
                            self.label_arr[each_row][each_col].grid(row=each_row,column=each_col)


                    
                    # Draw building
                    elif each_text[each_col] == 'U':
                        self.label_arr[each_row][each_col]  = tk.Label(self.root,text="U", relief=tk.SOLID, width=2, fg="white", bg="black", borderwidth=2, highlightcolor="orange")
                        self.label_arr[each_row][each_col].grid(row=each_row,column=each_col)
                    elif each_text[each_col] == 'O':
                        self.label_arr[each_row][each_col]  = tk.Label(self.root,text="O", relief=tk.SOLID, width=2, fg="white", bg="black", borderwidth=2, highlightcolor="orange")
                        self.label_arr[each_row][each_col].grid(row=each_row,column=each_col)
                    elif each_text[each_col] == 'H':
                        self.label_arr[each_row][each_col]  = tk.Label(self.root,text="H", relief=tk.SOLID, width=2, fg="white", bg="black", borderwidth=2, highlightcolor="orange")
                        self.label_arr[each_row][each_col].grid(row=each_row,column=each_col)

        #to print the rest of the states
        elif each_text_grid_itr < len(self.text_print_arr):
            each_text_grid_print = self.text_print_arr[each_text_grid_itr]
            each_text_grid_row_split = each_text_grid_print.split('\n')
            for each_row in range(len(each_text_grid_row_split)):
                each_text = each_text_grid_row_split[each_row]
                for each_col in range(len(each_text)):
                   # IF EMPTY
                    if each_text[each_col] == ' ':

                        building_list = self.check_facility_in_neighbourhood(each_row,each_col,self.model.radius)
                        if  not len(building_list)== 0:
                            self.label_arr[each_row][each_col]['text'] =  " "
                            self.label_arr[each_row][each_col]['relief'] = tk.SOLID
                            self.label_arr[each_row][each_col]['width'] =  2
                            self.label_arr[each_row][each_col]['fg'] =  "black"
                            self.label_arr[each_row][each_col]['bg'] =  "white"
                            self.label_arr[each_row][each_col]['borderwidth'] = 2

                            #tk.Label(self.root,text=" ", relief=tk.SOLID, width=2, fg="black", borderwidth=2).grid(row=each_row,column=each_col)
                        else:
                            self.label_arr[each_row][each_col]['text'] =  " "
                            self.label_arr[each_row][each_col]['relief'] = tk.RIDGE
                            self.label_arr[each_row][each_col]['bg'] =  "white"
                            self.label_arr[each_row][each_col]['width'] =  2

                            #tk.Label(self.root,text=" ", relief=tk.RIDGE, width=2).grid(row=each_row,column=each_col)

                    # IF STUDENT
                    elif each_text[each_col] == 'S':

                        building_list = self.check_facility_in_neighbourhood(each_row,each_col,self.model.radius)

                        if 0 in building_list:
                            self.label_arr[each_row][each_col]['text'] =  "U"
                            self.label_arr[each_row][each_col]['relief'] = tk.SOLID
                            self.label_arr[each_row][each_col]['width'] =  2
                            self.label_arr[each_row][each_col]['fg'] =  "white"
                            self.label_arr[each_row][each_col]['bg'] =  "green"
                            self.label_arr[each_row][each_col]['borderwidth'] = 2


                            #tk.Label(self.root,text="U", relief=tk.SOLID, width=2, fg="white", bg="green", borderwidth=2).grid(row=each_row,column=each_col)
                        elif not len(building_list)== 0:
                            self.label_arr[each_row][each_col]['text'] =  ""
                            self.label_arr[each_row][each_col]['relief'] = tk.SOLID
                            self.label_arr[each_row][each_col]['width'] =  2
                            self.label_arr[each_row][each_col]['fg'] =  "white"
                            self.label_arr[each_row][each_col]['bg'] =  "green"
                            self.label_arr[each_row][each_col]['borderwidth'] = 2


                            #tk.Label(self.root,text="", relief=tk.SOLID, width=2, fg="white",bg="green",borderwidth=2).grid(row=each_row,column=each_col)
                        else:
                            self.label_arr[each_row][each_col]['text'] =  ""
                            self.label_arr[each_row][each_col]['relief'] = tk.RIDGE
                            self.label_arr[each_row][each_col]['width'] =  2
                            self.label_arr[each_row][each_col]['bg'] =  "green"

                            #tk.Label(self.root,text="", relief=tk.RIDGE, width=2, bg="green").grid(row=each_row,column=each_col)

                    
                    # IF ADULT
                    elif each_text[each_col] == 'A':

                        building_list = self.check_facility_in_neighbourhood(each_row,each_col,self.model.radius)

                        if 1 in building_list:
                            self.label_arr[each_row][each_col]['text'] =  "O"
                            self.label_arr[each_row][each_col]['relief'] = tk.SOLID
                            self.label_arr[each_row][each_col]['width'] =  2
                            self.label_arr[each_row][each_col]['fg'] =  "white"
                            self.label_arr[each_row][each_col]['bg'] =  "blue"
                            self.label_arr[each_row][each_col]['borderwidth'] = 2

                            #tk.Label(self.root,text="O", relief=tk.SOLID, width=2, fg="white", bg="blue", borderwidth=2).grid(row=each_row,column=each_col)
                        elif not len(building_list)== 0:
                            self.label_arr[each_row][each_col]['text'] =  ""
                            self.label_arr[each_row][each_col]['relief'] = tk.SOLID
                            self.label_arr[each_row][each_col]['width'] =  2
                            self.label_arr[each_row][each_col]['fg'] =  "white"
                            self.label_arr[each_row][each_col]['bg'] =  "blue"
                            self.label_arr[each_row][each_col]['borderwidth'] = 2

                            #tk.Label(self.root,text="", relief=tk.SOLID, width=2, fg="white",bg="blue",borderwidth=2).grid(row=each_row,column=each_col)
                        else:
                            self.label_arr[each_row][each_col]['text'] =  ""
                            self.label_arr[each_row][each_col]['relief'] = tk.RIDGE
                            self.label_arr[each_row][each_col]['width'] =  2
                            self.label_arr[each_row][each_col]['bg'] =  "blue"

                            #tk.Label(self.root,text="", relief=tk.RIDGE, width=2, bg="blue").grid(row=each_row,column=each_col)
                        
                    # IF ELDERLY
                    elif each_text[each_col] == 'E':

                        building_list = self.check_facility_in_neighbourhood(each_row,each_col,self.model.radius)

                        if 2 in building_list:
                            self.label_arr[each_row][each_col]['text'] =  "H"
                            self.label_arr[each_row][each_col]['relief'] = tk.SOLID
                            self.label_arr[each_row][each_col]['width'] =  2
                            self.label_arr[each_row][each_col]['fg'] =  "white"
                            self.label_arr[each_row][each_col]['bg'] =  "red"
                            self.label_arr[each_row][each_col]['borderwidth'] = 2
                            


                            #tk.Label(self.root,text="H", relief=tk.SOLID, width=2, fg="white", bg="red", borderwidth=2).grid(row=each_row,column=each_col)
                        elif not len(building_list)== 0:
                            self.label_arr[each_row][each_col]['text'] =  ""
                            self.label_arr[each_row][each_col]['relief'] = tk.SOLID
                            self.label_arr[each_row][each_col]['width'] =  2
                            self.label_arr[each_row][each_col]['fg'] =  "white"
                            self.label_arr[each_row][each_col]['bg'] =  "red"
                            self.label_arr[each_row][each_col]['borderwidth'] = 2

                            #tk.Label(self.root,text="", relief=tk.SOLID, width=2, fg="white",bg="red",borderwidth=2).grid(row=each_row,column=each_col)
                        else:
                            self.label_arr[each_row][each_col]['text'] =  ""
                            self.label_arr[each_row][each_col]['relief'] = tk.RIDGE
                            self.label_arr[each_row][each_col]['width'] =  2
                            self.label_arr[each_row][each_col]['bg'] =  "red"

                            #tk.Label(self.root,text="", relief=tk.RIDGE, width=2, bg="red").grid(row=each_row,column=each_col)


                    
                    # Draw building
                    elif each_text[each_col] == 'U':
                        self.label_arr[each_row][each_col]['text'] =  "U"
                        self.label_arr[each_row][each_col]['relief'] = tk.SOLID
                        self.label_arr[each_row][each_col]['width'] =  2
                        self.label_arr[each_row][each_col]['fg'] =  "white"
                        self.label_arr[each_row][each_col]['bg'] =  "black"
                        self.label_arr[each_row][each_col]['borderwidth'] = 2
                        self.label_arr[each_row][each_col]['highlightcolor'] = "orange"

                        #tk.Label(self.root,text="U", relief=tk.SOLID, width=2, fg="white", bg="black", borderwidth=2, highlightcolor="orange").grid(row=each_row,column=each_col)
                    elif each_text[each_col] == 'O':
                        self.label_arr[each_row][each_col]['text'] =  "O"
                        self.label_arr[each_row][each_col]['relief'] = tk.SOLID
                        self.label_arr[each_row][each_col]['width'] =  2
                        self.label_arr[each_row][each_col]['fg'] =  "white"
                        self.label_arr[each_row][each_col]['bg'] =  "black"
                        self.label_arr[each_row][each_col]['borderwidth'] = 2
                        self.label_arr[each_row][each_col]['highlightcolor'] = "orange"

                        #tk.Label(self.root,text="O", relief=tk.SOLID, width=2, fg="white", bg="black", borderwidth=2, highlightcolor="orange").grid(row=each_row,column=each_col)
                    elif each_text[each_col] == 'H':
                        self.label_arr[each_row][each_col]['text'] =  "H"
                        self.label_arr[each_row][each_col]['relief'] = tk.SOLID
                        self.label_arr[each_row][each_col]['width'] =  2
                        self.label_arr[each_row][each_col]['fg'] =  "white"
                        self.label_arr[each_row][each_col]['bg'] =  "black"
                        self.label_arr[each_row][each_col]['borderwidth'] = 2
                        self.label_arr[each_row][each_col]['highlightcolor'] = "orange"

                        #tk.Label(self.root,text="H", relief=tk.SOLID, width=2, fg="white", bg="black", borderwidth=2, highlightcolor="orange").grid(row=each_row,column=each_col)

            each_text_grid_itr = each_text_grid_itr + 1
            self.root.after(1000, self.text_gui,each_text_grid_itr)

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
                if c.type == 0:
                    text += 'U'
                elif c.type == 1:
                    text += 'O'
                elif c.type == 2:
                    text += 'H'
            else:
                if c.type == 0:
                    text += 'S'
                elif c.type == 1:
                    text += 'A'
                elif c.type == 2:
                    text += 'E'
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
