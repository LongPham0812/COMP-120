"""
Module: Snake2

Authors: Long Pham and Eric Pan

Emails: longpham@sandiego.edu and epan@sandiego.edu

Date: November 21, 2021

Description: A Python implementation of greedy snake using Tkinter and implemented
using the model-view-controller design pattern.

Iteration 2:
Displays the grid in the grid frame, with each cell of the grid its own frame.

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
        # Define parameters
        self.NUM_ROWS = 30
        self.NUM_COLS = 30

        # Create view
        self.view = SnakeView(self.NUM_ROWS, self.NUM_COLS)

        # Start the simulation
        self.view.window.mainloop()

class SnakeView:
    def __init__(self, num_rows, num_cols):
        """ Initialize view of the game """
        # Constants
        self.CELL_SIZE = 20
        self.CONTROL_FRAME_HEIGHT = 100
        self.SCORE_FRAME_WIDTH = 200

        # Size of grid
        self.num_rows = num_rows
        self.num_cols = num_cols

        # Create window
        self.window = tk.Tk()
        self.window.title("Greedy Snake")

        # Create frame for grid of cells, and put cells in the frame
        self.grid_frame = tk.Frame(self.window, height = num_rows * self.CELL_SIZE,
                                width = num_cols * self.CELL_SIZE)
        self.grid_frame.grid(row = 1, column = 1) # use grid layout manager
        self.cells = self.add_cells()

        # Create frame for controls
        self.control_frame = tk.Frame(self.window, width = num_cols * self.CELL_SIZE + self.SCORE_FRAME_WIDTH, 
                                height = self.CONTROL_FRAME_HEIGHT, bg = 'blue')
        self.control_frame.grid(row = 2, column = 1, columnspan= 2) # use grid layout manager

        #Create frame for scoreboard
        self.score_frame = tk.Frame(self.window, width =self.SCORE_FRAME_WIDTH, height = num_rows * self.CELL_SIZE,
                                bg = 'green')  
        self.score_frame.grid(row = 1, column = 2) # use grid layout manager

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

class SnakeModel:
    def __init__(self, num_rows, num_cols):
        """ initialize the model of the game """

if __name__ == "__main__":
    # Play the game
    snake_game = Snake()