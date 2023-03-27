"""
Module: Snake5

Authors: Long Pham and Eric Pan

Emails: longpham@sandiego.edu and epan@sandiego.edu

Date: November 23, 2021

Description: A Python implementation of greedy snake using Tkinter and implemented
using the model-view-controller design pattern.

Iteration 5:
Connects user actions performed on the controls (in the SnakeView class)
to handler functions in the controller (the Snake class).

For now, the handler functions are just stubs that print a message indicating
they have been called. This allows validating that the connection between
a user action and a function in the controller has been made.

"""
import random
import tkinter as tk
from tkinter.font import Font
from enum import Enum
import time

class Snake:
    """ This is the controller """
    def __init__(self):
        """ Initializes the snake game """
        self.NUM_ROWS = 30
        self.NUM_COLS = 30

        self.view = SnakeView(self.NUM_ROWS, self.NUM_COLS)
        #Sets handlers to a method
        self.view.set_start_handler(self.start_handler)
        self.view.set_pause_handler(self.pause_handler)
        self.view.set_step_speed_handler(self.step_speed_handler)
        self.view.set_reset_handler(self.reset_handler)
        self.view.set_quit_handler(self.quit_handler)
        self.view.set_wraparound_handler(self.wraparound_handler)

        self.view.set_left_handler(self.left_handler)
        self.view.set_right_handler(self.right_handler)
        self.view.set_up_handler(self.up_handler)
        self.view.set_down_handler(self.down_handler)

        self.view.window.mainloop()

    def start_handler(self):
        """ Starts snake game """
        print("Start simulation")

    def pause_handler(self):
        """ Pauses snake game """
        print("Pause simulation")

    def step_speed_handler(self, value):
        """ Speeds up or slows down snake """
        print("Step speed: value = %s" % (value))

    def reset_handler(self):
        """ Resets snake game """
        print("Reset simulation")

    def quit_handler(self):
        """ Quits snake game """
        print("Quit program")

    def wraparound_handler(self):
        """ Option for snake to go past boundary """
        print("Wraparound box clicked")

    def left_handler(self, event):
        """ Snake turns left """
        print("Left button pressed")

    def right_handler(self, event):
        """ Snake turns right """
        print("Right button pressed")

    def up_handler(self, event):
        """ Snake turns up """
        print("Up button pressed")

    def down_handler(self, event):
        """ Snake turns down """
        print("Down button pressed")

class SnakeView:
    def __init__(self, num_rows, num_cols):
        """ Initialize view of the game """
        self.CELL_SIZE = 20
        self.CONTROL_FRAME_HEIGHT = 100
        self.SCORE_FRAME_WIDTH = 200

        self.num_rows = num_rows
        self.num_cols = num_cols

        self.window = tk.Tk()
        self.window.title("Greedy Snake")

        # Create frame for grid of cells, and put cells in the frame
        self.grid_frame = tk.Frame(self.window, height = num_rows * self.CELL_SIZE,
                                width = num_cols * self.CELL_SIZE)
        self.grid_frame.grid(row = 1, column = 1) # use grid layout manager
        self.cells = self.add_cells()

        # Create frame for controls
        self.control_frame = tk.Frame(self.window, width = num_cols * self.CELL_SIZE + self.SCORE_FRAME_WIDTH, 
                                height = self.CONTROL_FRAME_HEIGHT)
        self.control_frame.grid(row = 2, column = 1, columnspan= 2) # use grid layout manager
        self.control_frame.grid_propagate(False)
        (self.start_button, self.pause_button, 
         self.step_speed_slider, self.reset_button, 
         self.quit_button, self.wraparound_button) = self.add_control()

        #Create frame for scoreboard
        self.score_frame = tk.Frame(self.window, width =self.SCORE_FRAME_WIDTH, 
                                height = num_rows * self.CELL_SIZE, borderwidth = 1, relief = "solid")  
        self.score_frame.grid(row = 1, column = 2)
        self.score_frame.grid_propagate(False)
        (self.score_label, self.points_frame, self.time_frame,
        self.pts_sec_frame, self.game_over_label) = self.add_score()

    def add_cells(self):
        """ Add cells to the grid frame """
        cells = []
        for r in range(self.num_rows):
            row = []
            for c in range(self.num_cols):
                frame = tk.Frame(self.grid_frame, width = self.CELL_SIZE, 
                           height = self.CELL_SIZE, borderwidth = 1, 
                           relief = "solid")
                frame.grid(row = r, column = c) # use grid layout manager
                row.append(frame)
            cells.append(row)
        return cells

    def add_control(self):
        """ 
        Create control buttons and slider, and add them to the control frame 
        """
        start_button = tk.Button(self.control_frame, text="Start")
        start_button.grid(row=1, column=1, padx = 25)
        pause_button = tk.Button(self.control_frame, text="Pause")
        pause_button.grid(row=1, column=2, padx = 25)
        step_speed_slider = tk.Scale(self.control_frame, from_=1, to=10, 
                    label="Step Speed", showvalue=0, orient=tk.HORIZONTAL)
        step_speed_slider.grid(row=1, column=3, padx = 25)
        reset_button = tk.Button(self.control_frame, text="Reset")
        reset_button.grid(row=1, column=4, padx = 25)
        quit_button = tk.Button(self.control_frame, text="Quit")
        quit_button.grid(row=1, column=5, padx = 25)
        wraparound_button = tk.Checkbutton(self.control_frame, text = "Wraparound")
        wraparound_button.grid(row = 1, column = 6, padx = 25)
        # Vertically center the controls in the control frame
        self.control_frame.grid_rowconfigure(1, weight = 1) 
        # Horizontally center the controls in the control frame
        self.control_frame.grid_columnconfigure(0, weight = 1) 
        self.control_frame.grid_columnconfigure(7, weight = 1) 
                                                            
        return (start_button, pause_button, step_speed_slider, 
                reset_button, quit_button, wraparound_button)

    def add_score(self):
        """ 
        Create score counter label, timer label, average score per second label,
        game over label, and adds them to the score frame 
        """
        score_label = tk.Label(self.score_frame, text = "Score")
        score_label.grid(row = 1, column = 1)
        #Points counter label
        points_frame = tk.Frame(self.score_frame, borderwidth = 1, relief = "solid")
        points_frame.grid(row = 2, column = 1, pady = 25)
        points_label = tk.Label(points_frame, text = "Points:")
        points_label.grid(row = 1, column = 1)
        points_num = tk.Label(points_frame, text = "0")
        points_num.grid(row = 1, column = 2)
        #timer label
        time_frame = tk.Frame(self.score_frame, borderwidth = 1, relief = "solid")
        time_frame.grid(row = 3, column = 1, pady = 25)
        time_label = tk.Label(time_frame, text = "Time:")
        time_label.grid(row = 1, column =  1)
        time_num = tk.Label(time_frame, text = "0.00")
        time_num.grid(row = 1, column = 2)
        #Points per second label
        pts_sec_frame = tk.Frame(self.score_frame, borderwidth = 1, relief = "solid")
        pts_sec_frame.grid(row = 4, column = 1, pady = 25)
        pts_sec_label = tk.Label(pts_sec_frame, text = "Points per sec:")
        pts_sec_label.grid(row = 1, column = 1)
        pts_sec_num = tk.Label(pts_sec_frame, text = "0.00")
        pts_sec_num.grid(row = 1, column = 2)
        #Game over label
        game_over_label = tk.Label(self.score_frame)
        game_over_label.grid(row = 5, column = 1, pady = 25)

        self.score_frame.grid_columnconfigure(1, weight = 1)

        return(score_label, points_frame, time_frame, 
                pts_sec_frame, game_over_label)

    def set_start_handler(self, handler):
        """ Assigns start button to start handler """
        self.start_button.configure(command = handler)

    def set_pause_handler(self, handler):
        """ Assigns pause button to pause handler """
        self.pause_button.configure(command = handler)

    def set_step_speed_handler(self, handler):
        """ Assigns step speed button to step speed handler """
        self.step_speed_slider.configure(command = handler)

    def set_reset_handler(self, handler):
        """ Assigns reset button to start handler """
        self.reset_button.configure(command = handler)

    def set_quit_handler(self, handler):
        """ Assigns start button to start handler """
        self.quit_button.configure(command = handler)

    def set_wraparound_handler(self, handler):
        """ Assigns wraparound button to wraparound handler """
        self.wraparound_button.configure(command = handler)

    def set_left_handler(self, handler):
        """ Assigns left arrow key button to left arrow key handler """
        self.window.bind('<Left>', handler)

    def set_right_handler(self, handler):
        """ Assigns right arrow key button to right arrow key handler """
        self.window.bind('<Right>', handler)

    def set_up_handler(self, handler):
        """ Assigns up arrow key button to up arrow key handler """
        self.window.bind('<Up>', handler)

    def set_down_handler(self, handler):
        """ Assigns down arrow key button to down arrow key handler """
        self.window.bind('<Down>', handler)

class SnakeModel:
    def __init__(self, num_rows, num_cols):
        """ initialize the model of the game """

if __name__ == "__main__":
   snake_game = Snake()