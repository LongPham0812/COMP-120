# File: display_clock.py
# Author: Long Pham and Scott Schnieders
# Date: 10/7/2021
# Description: Program that displays clock as well as
# time in numbers. Also has buttons that stop and start
# the clock and quit the program.

import math
import datetime
import tkinter as tk
from enum import Enum

class Display_Clock:
    
    def __init__(self):
        self.window = tk.Tk() # Create a window
        self.window.title("Current Time") # Set a title
        self.window.geometry("220x270")

        self.clock_radius_size = 0.8 # Create instance variables
        self.canvas_size = 200
        self.second_size = 0.8
        self.center = (self.canvas_size // 2)
        self.minute_size = 0.65
        self.hour_size = 0.5
        self.time_between = 1000
        self.state = State.GOING
        self.current_time = datetime.datetime.now()
        self.hour = 0
        self.minute = 0
        self.second = 0
        self.get_time()

        self.create_layout()

        self.update_clock()
        self.window.mainloop()
    
    def create_layout(self):
        self.frame_canvas = tk.Frame(self.window) # Create a canvas + frame for canvas
        self.frame_canvas.pack()

        self.canvas = tk.Canvas(height = self.canvas_size, width = self.canvas_size) 
        self.canvas.pack()

        self.canvas.create_oval(self.center - (self.clock_radius_size * self.center), self.center - (self.clock_radius_size * self.center), self.center + (self.clock_radius_size * self.center), self.center + (self.clock_radius_size * self.center), tags = "all")
        self.clock_radius = self.clock_radius_size * self.center
        self.canvas.create_text(self.center, self.center - (self.clock_radius_size * self.center) + 6, text = "12", tags = "all")
        self.canvas.create_text(self.center, self.center + (self.clock_radius_size * self.center) - 6, text = "6", tags = "all")
        self.canvas.create_text(self.center + (self.clock_radius_size*self.center) - 6, self.center, text = "3", tags = "all")
        self.canvas.create_text(self.center - (self.clock_radius_size*self.center) + 6, self.center, text = "9", tags = "all")
        self.draw_hands() # Create the clock

        self.frame_label = tk.Frame(self.window) # Create frame for numeric form of time + label for time
        self.frame_label.pack()

        self.timeLabel = tk.Label(self.frame_label, text = str(self.hour) + ":" + f'{self.minute:02}' + ":" + f'{self.second:02}')
        self.timeLabel.grid(row = 1, column = 1)

        self.frame_buttons = tk.Frame(self.window) # Create frame for buttons + buttons themselves
        self.frame_buttons.pack()

        self.stop_button = tk.Button(self.frame_buttons, text = "Stop", command = self.stop_handler)
        self.stop_button.grid(row = 1, column = 1)
        self.quit_button = tk.Button(self.frame_buttons, text = "Quit", command = self.quit_handler)
        self.quit_button.grid(row = 1, column = 2)

    def get_time(self):
        self.current_time = datetime.datetime.now() # Get current time
        self.hour = self.current_time.hour
        if self.hour > 12:
            self.hour -= 12
        self.minute = self.current_time.minute
        self.second = self.current_time.second
    
    def draw_hands(self):
        self.canvas.delete("hands") # Calculate angles + change in angles and update hands accordingly
        second_reference = 6 * 2 * math.pi / 360
        minute_reference = 0.1 * 2 * math.pi / 360
        hour_reference = 2 * math.pi / 43200
        second_angle = second_reference * (self.second + 45)
        minute_angle = minute_reference * ((self.minute + (self.second / 60)) * 60 + 2700)
        hour_angle = hour_reference * ((self.hour + (self.second / 3600) + (self.minute / 60)) * 3600 + 32400)
        self.canvas.create_line(self.center, self.center, self.center + (math.cos(hour_angle)) * (self.hour_size * self.clock_radius), self.center + (math.sin(hour_angle)) * (self.hour_size * self.clock_radius), fill = "green", tags = "hands")
        self.canvas.create_line(self.center, self.center, self.center + (math.cos(minute_angle)) * (self.minute_size * self.clock_radius), self.center + (math.sin(minute_angle)) * (self.minute_size * self.clock_radius), fill = "blue", tags = "hands")
        self.canvas.create_line(self.center, self.center, self.center + (math.cos(second_angle)) * (self.second_size * self.clock_radius), self.center + (math.sin(second_angle)) * (self.second_size * self.clock_radius), fill = "red", tags = "hands")

    def update_clock(self):
        self.timer = self.canvas.after(self.time_between, self.update_clock) # Update clock + time
        self.get_time()
        self.timeLabel['text'] = str(self.hour) + ":" + f'{self.minute:02}' + ":" + f'{self.second:02}'
        self.draw_hands()
        
    def stop_handler(self):
        self.stop_button.destroy() # Stop clock movement
        self.start_button = tk.Button(self.frame_buttons, text = "Start", command = self.start_handler)
        self.start_button.grid(row = 1, column = 1)
        if self.state == State.GOING:
            self.window.after_cancel(self.timer)
            self.state = State.NOT_GOING

    def start_handler(self):
        self.start_button.destroy() # Start clock movement
        self.stop_button = tk.Button(self.frame_buttons, text = "Stop", command = self.stop_handler)
        self.stop_button.grid(row = 1, column = 1)
        if self.state == State.NOT_GOING:
            self.update_clock()
            self.state = State.GOING
    
    def quit_handler(self):
        # Quit the program
        self.canvas.delete("all")
        self.canvas.delete("hands")
        self.window.destroy()

class State(Enum):
    GOING = 1 # Numbers to determine whether the clock is moving or not
    NOT_GOING = 2
        
if __name__ == "__main__":
    Display_Clock()
