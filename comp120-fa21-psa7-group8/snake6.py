"""
Module: Snake6

Authors: Long Pham and Eric Pan

Emails: longpham@sandiego.edu and epan@sandiego.edu

Date: November 24, 2021

Description: A Python implementation of greedy snake using Tkinter and implemented
using the model-view-controller design pattern.

Iteration 6:
Adds the SnakeModel class that represents the grid of the game. This is the 
model part of the model-view-controller.

Also, add code (the class SnakeModelTest) to unit test the SnakeModel class, as the
game is not playable yet (the event handler functions are still stubs), and so 
the snake model cannot be validated visually.
"""
import random
import tkinter as tk
from tkinter.font import Font
from enum import IntEnum
import time
import unittest

class Snake:
    """ This is the controller """
    def __init__(self):
        """ Initializes the snake game """
        self.NUM_ROWS = 30
        self.NUM_COLS = 30

        self.model = SnakeModel(self.NUM_ROWS, self.NUM_COLS)
        self.view = SnakeView(self.NUM_ROWS, self.NUM_COLS)

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
        direction = "LEFT"
        #Assigns direction to the current direction of snake
        self.model.make_direction(direction)
        print("Left button pressed")

    def right_handler(self, event):
        """ Snake turns right """
        direction = "RIGHT"
        self.model.make_direction(direction)
        print("Right button pressed")

    def up_handler(self, event):
        """ Snake turns up """
        direction = "UP"
        self.model.make_direction(direction)
        print("Up button pressed")

    def down_handler(self, event):
        """ Snake turns down """
        direction = "DOWN"
        self.model.make_direction(direction)
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
        self.num_rows = num_rows
        self.num_cols = num_cols
        #Initializes state for cells in grid
        self.state = [[CellState.EMPTY for c in range(self.num_cols)] 
                        for r in range(self.num_rows)]

        self.snake = []
        #Gets random coordinate for snake
        snake_x = random.randrange(0, self.num_cols)
        snake_y = random.randrange(0, self.num_rows)
        #Intializes snake head for unit testing
        snake_head = self.make_snake(4, 3)

        self.snake.append(snake_head)
        #Gets random coordinate for food
        food_x = random.randrange(0, self.num_cols)
        food_y = random.randrange(0, self.num_rows)
        #Intializes food for unit testing
        self.food = self.make_food(4, 2)

        self.direction = None
    
    def make_direction(self, direction):
        """ Assigns direction used for unit testing """
        self.direction = direction

    def make_snake(self, row, col):
        """ Make the cell in row, col alive. """
        self.state[row][col] = CellState.SNAKE
        return [row, col]
    
    def make_empty(self, row, col):
        """ Make the cell in row, col empty. """
        self.state[row][col] = CellState.EMPTY

    def make_food(self, row, col):
        """ Creates random food cordinate """
        while (row, col) in self.snake:
            row = random.randrange(0, self.num_cols)
            col = random.randrange(0, self.num_rows)
        #Changes state of cell of food to food
        self.state[row][col] = CellState.FOOD
        return [row, col]

    def is_snake(self, row, col):
        """ Checks if cell is part of the snake """
        return self.state[row][col] == CellState.SNAKE

    def is_food(self, row, col):
        """ Checks if cell is food """
        return self.state[row][col] == CellState.FOOD

    def reset(self):
        """ Resets grid to all empty """
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                self.make_empty(r, c)

    def one_step(self):
        """ One step of the game """
        next_state = [[CellState.EMPTY for c in range(self.num_cols)] 
                        for r in range(self.num_rows)]

        #Moves snake body by adding temp variable
        #to store prev square location.
        for s in range(0, len(self.snake) - 1):
            #Last coordinate of snake will become empty for each step.
            if s == 0:
                #Assigns last coordinate to empty tail.
                empty_tail = self.snake[len(self.snake) - 1]
            #Moves snake and assigns snake to grid
            self.snake[len(self.snake) - 1 - s] = self.snake[len(self.snake) - 2 - s]
            next_state[self.snake[len(self.snake) - 1 - s][0]][self.snake[len(self.snake) - 1 - s][1]] = CellState.SNAKE
        #Empty tail becomes empty
        if len(self.snake) > 1:
            next_state[empty_tail[0]][empty_tail[1]] = 0

        #Makes new snake head in the direction of user's choice.
        next_state[self.snake[0][0]][self.snake[0][1]] = CellState.EMPTY
        if self.direction == "UP":
            self.snake[0][0] = self.snake[0][0] - 1
        elif self.direction == "RIGHT":
            self.snake[0][1] = self.snake[0][1] + 1
        elif self.direction == "DOWN":
            self.snake[0][0] = self.snake[0][0] + 1
        elif self.direction == "LEFT":
            self.snake[0][1] = self.snake[0][1] - 1
        next_state[self.snake[0][0]][self.snake[0][1]] = CellState.SNAKE

        #Checks if snake eats apple
        if self.is_food(self.snake[0][0], self.snake[0][1]):
            # length 1 --> add body depending on direction.
            if len(self.snake) == 1:
                if self.direction == "UP":
                    self.snake.append(self.make_snake(self.snake[0][0] + 1, self.snake[0][1]))
                elif self.direction == "RIGHT":
                    self.snake.append(self.make_snake(self.snake[0][0], self.snake[0][1] - 1))
                elif self.direction == "DOWN":
                    self.snake.append(self.make_snake(self.snake[0][0] - 1, self.snake[0][1]))
                elif self.direction == "LEFT":
                    self.snake.append(self.make_snake(self.snake[0][0], self.snake[0][1] + 1))
                next_state[self.snake[1][0]][self.snake[1][1]] = CellState.SNAKE
            else:
                #Adds snake body to the last previous coordinate of snake when apple is eaten.
                self.snake.append(self.make_snake(empty_tail[0],empty_tail[1]))
            food_x = random.randrange(0, self.num_cols)
            food_y = random.randrange(0, self.num_rows)
            #Assigns food for unit testing
            self.food = self.make_food(5, 5)
            next_state[self.food[0]][self.food[1]] = CellState.FOOD
        #Updates state for unit testing
        self.state = next_state
        
class CellState(IntEnum):
    """ 
    Use IntEnum so that the test code below can
    set cell states using 0's and 1's
    """
    EMPTY = 0
    SNAKE = 1
    FOOD = 2

class SnakeModelTest(unittest.TestCase):
    """ Tests one step of the game """
    def setUp(self):
        #Run in termintal: python3 -m unittest snake6.py
        #to check if one step of the game is valid.
        self.model = SnakeModel(10, 10)
        #Initalizes the direction of the snake to go left
        self.model.make_direction("LEFT")
        #Initial state of game
        self.model.state = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 2, 1, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        #State of game after snake moves left and eats apple
        self.correct_next_state = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    def test_one_step(self):
        """ Tests one step of the game """
        self.model.one_step()
        self.assertEqual(self.model.state, self.correct_next_state)

if __name__ == "__main__":
   snake_game = Snake()