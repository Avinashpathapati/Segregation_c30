from model import Model
import tkinter as tk


class Visualization():
    def __init__(self, model):
        # Initialize model
        self.model = model
        #self.root.after(20,self.render)
        self.root = tk.Tk()
        self.text_print_arr = []
        self.render()

    def step(self):
        self.model.step()
        self.render()
        #self.render()

    # Print ascii text of 2D grid
    def render(self):
        text = ""
        for y in range(self.model.grid.height):
            for x in range(self.model.grid.width):
                c = self.model.grid[y][x]
                if c is None:
                    text += ' '
                elif c.type == 0:
                    text += 'X'
                elif c.type == 1:
                    text += '0'
                else:
                    text += '+'
                # c = self.model.grid[y][x]
                # if c is None:
                #     tk.Label(root,text=" ", relief=tk.RIDGE, width=15).grid(row=y,column=x)
                # elif c.type == 0:
                #     tk.Label(root,text="X", relief=tk.RIDGE, width=15, fg="red").grid(row=y,column=x)
                # elif c.type == 1:
                #     tk.Label(root,text="O", relief=tk.RIDGE, width=15, fg="green").grid(row=y,column=x)
                # else:
                #     tk.Label(root,text="+", relief=tk.RIDGE, width=15, fg="red").grid(row=y,column=x)

        # root.after(1000, lambda: root.destroy())
        # tk.mainloop()

            text += '\n'
        self.text_print_arr.append(text)
        #print(text)

    def print_text_grid(self):

        #to perform the first iteration
        self.text_gui(0)
        #to update the same window again and again
        self.root.after(3000, self.text_gui,1)
        #to destroy finally
        #self.root.after(1000, lambda: self.root.destroy())


    def text_gui(self,each_text_grid_itr):

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
                    else:
                        tk.Label(self.root,text="+", relief=tk.RIDGE, width=15, fg="red").grid(row=each_row,column=each_col)


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
                    else:
                        tk.Label(self.root,text="+", relief=tk.RIDGE, width=15, fg="red").grid(row=each_row,column=each_col)

        
            each_text_grid_itr = each_text_grid_itr + 1
            self.root.after(1000,self.text_gui,each_text_grid_itr)

        elif each_text_grid_itr == len(self.text_print_arr):
            #self.root.after(1000, lambda: self.root.destroy())
            each_text_grid_itr = each_text_grid_itr + 1




# Initialize input parameters of model
if __name__ == '__main__':
    model_params = {
        "height": 10,
        "width": 10,
        # Agent density, from 0.8 to 1.0
        "density": 0.8,
        # Homophily, from 2 to 8
        "homophily": 2
    }

    model = Model(**model_params)
    viz = Visualization(model)

    # Run the model for 100 epochs
    for i in range(100):
        if model.running:
            print("Step:", i)
            viz.step()
            print('----')

    
    viz.print_text_grid()
    #viz.root.after(1000, lambda: viz.root.destroy())

    viz.root.mainloop()
    
    

    
