# File: addressbook.py
# Author: Long Pham and Scott Schnieders
# Date: 9/30/21
# Description: This is a program where the user can enter information about an address. There are multiple buttons
# the user can use to access and navigate through the list of addresses entered. The user can also save and load
# files with addresses.

import tkinter as tk

class Address:
    def __init__(self, name, street, city, state, zip):
        """ 
        Constructor for Address class.
        You will add parameters to this constructor. 
        """
        self.name = name
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip

    # You may add other methods.

class AddressBook: # AddressBook layout
    def __init__(self):
        """ Constructor for AddressBook class """

        # Create window.
        self.window = tk.Tk()  
        self.window.title("AddressBook") 
        self.entries = []
        self.cIndex = 0

        self.window.geometry("285x120")
        
        self.topFrame = tk.Frame(self.window)
        self.topFrame.grid(row=1,column=1)

        self.middleFrame = tk.Frame(self.window)
        self.middleFrame.grid(row=2,column=1)

        self.bottomFrame = tk.Frame(self.window)
        self.bottomFrame.grid(row=3,column=1)

        # Add labels and entries for the 5 parts of the address
        self.name_label = tk.Label(self.topFrame, text = "Name")
        self.name_label.grid(row = 1, column = 1)
        
        self.street_label = tk.Label(self.topFrame, text = "Street")
        self.street_label.grid(row = 2, column = 1)

        self.name_var = tk.StringVar()  # A special string variable that will be associated
        self.name = tk.Entry(self.topFrame, width=35, textvariable=self.name_var)
        self.name.grid(row = 1, column = 2, columnspan = 6)

        self.street_var = tk.StringVar()  # A special string variable that will be associated
        self.street = tk.Entry(self.topFrame, width=35, textvariable=self.street_var)
        self.street.grid(row = 2, column = 2, columnspan = 6)

        self.city_label = tk.Label(self.topFrame, text = "City")
        self.city_label.grid(row = 3, column = 1)
        self.city_var = tk.StringVar()  # A special string variable that will be associated
        self.city = tk.Entry(self.topFrame, width=15,textvariable=self.city_var)
        self.city.grid(row = 3, column = 2)

        self.state_label = tk.Label(self.topFrame, text = "State")
        self.state_label.grid(row = 3, column = 3)
        self.state_var = tk.StringVar()  # A special string variable that will be associated
        self.state = tk.Entry(self.topFrame, width=5, textvariable=self.state_var)
        self.state.grid(row = 3, column = 4)

        self.zip_label = tk.Label(self.topFrame, text = "Zip")
        self.zip_label.grid(row = 3, column = 5)
        self.zip_var = tk.StringVar()  # A special string variable that will be associated
        self.zip = tk.Entry(self.topFrame, width=5, textvariable=self.zip_var)
        self.zip.grid(row = 3, column = 6)

        # Add buttons associated with the address book program
        self.add_button = tk.Button(self.middleFrame, text = "Add", command=self.add_handler)
        self.add_button.grid(row = 1, column = 2)

        self.delete_button = tk.Button(self.middleFrame, text = "Delete", command=self.delete_handler)
        self.delete_button.grid(row = 1, column = 3)

        self.first_button = tk.Button(self.middleFrame, text = "First", command=self.first_handler)
        self.first_button.grid(row = 1, column = 4)

        self.next_button = tk.Button(self.middleFrame, text = "Next", command=self.next_handler)
        self.next_button.grid(row = 1, column = 5)

        self.previous_button = tk.Button(self.middleFrame, text = "Previous", command=self.previous_handler)
        self.previous_button.grid(row = 1, column = 6)

        self.last_button = tk.Button(self.middleFrame, text = "Last", command=self.last_handler)
        self.last_button.grid(row = 1, column = 7)

        self.filename_label = tk.Label(self.bottomFrame, text = "Filename")
        self.filename_label.grid(row = 1, column = 1)
        self.filename_var = tk.StringVar()
        self.filename_entry = tk.Entry(self.bottomFrame, width=10, textvariable=self.filename_var)
        self.filename_entry.grid(row = 1, column = 2)

        self.load_file_button = tk.Button(self.bottomFrame, text = "Load File", command=self.load_file_handler)
        self.load_file_button.grid(row = 1, column = 3)

        self.save_to_file_button = tk.Button(self.bottomFrame, text = "Save to File", command=self.save_file_handler)
        self.save_to_file_button.grid(row = 1, column = 4)

        self.quit_button = tk.Button(self.bottomFrame, text = "Quit", command=self.quit_handler)
        self.quit_button.grid(row = 1, column = 5)

        # You will add code here.
    def add_handler(self):
        """ adds the currently displayed address to the list of
        addresses, directly after the currently displayed address,
        or to the front of the list, if the list is empty and no
        address is being displayed.  """
        temp = Address(self.name_var.get(), self.street_var.get(), self.city_var.get(), self.state_var.get(), self.zip_var.get())
        if len(self.entries) > self.cIndex:
            self.entries.insert(self.cIndex + 1, temp)
            self.cIndex +=1
        else:
            self.entries.append(temp)

        self.setFields(self.entries[self.cIndex])
    
    def delete_handler(self):
        """ deletes currently displayed address and displays 
        an adjacent address in the list depending on the address
        that was deleted. """
        if len(self.entries) > 0 and self.cIndex < len(self.entries) - 1:
            self.entries.remove(self.entries[self.cIndex])
            self.setFields(self.entries[self.cIndex])
        elif len(self.entries) > 0 and self.cIndex == len(self.entries) - 1:
            self.entries.remove(self.entries[self.cIndex])
            self.setFields(self.entries[self.cIndex - 1])
        else:
            self.dispNot()

    def first_handler(self):
        """displays the first address in the list, or nothing if the
        list of addresses is empty."""
        if len(self.entries) > 0:
            first = self.entries[0]
            self.cIndex = 0
            self.setFields(first)

    def next_handler(self):
        """displays the next address in the list. If there is not
        a next address, do nothing."""
        if len(self.entries) > self.cIndex + 1:
            self.cIndex += 1
            self.setFields(self.entries[self.cIndex])
        elif len(self.entries) == 0:
            pass
        elif len(self.entries) <= self.cIndex:
            self.setFields(self.entries[self.cIndex - 1])

    def previous_handler(self):
        """displays the previous address in the list. If
        there is not a previous address, do nothing."""
        if 0 <= self.cIndex-1:
            self.cIndex -= 1
            self.setFields(self.entries[self.cIndex])
        elif len(self.entries) == 1:
            self.setFields(self.entries[0])

    def last_handler(self):
        """displays the last address in the list, or nothing if the
        list is empty."""
        if len(self.entries) > 0:
            last = self.entries[-1]
            self.cIndex = len(self.entries) - 1
            self.setFields(last)

    def load_file_handler(self):
        """loads file that was entered in the filename entry"""
        try:
            file = open(self.filename_var.get(), "r")
            self.entries.clear()
            self.name_var.set(file.readline().strip())
            self.street_var.set(file.readline().strip())
            self.city_var.set(file.readline().strip())
            self.state_var.set(file.readline().strip())
            self.zip_var.set(file.readline().strip())
            self.entries.append(Address(self.name_var.get(), self.street_var.get(), self.city_var.get(), self.state_var.get(), self.zip_var.get()))

            line = file.readline().strip()
            while line != "":
                self.name_in = line
                line = file.readline().strip()
                self.street_in = line
                line = file.readline().strip()
                self.city_in = line
                line = file.readline().strip()
                self.state_in = line
                line = file.readline().strip()
                self.zip_in = line
                self.entries.append(Address(self.name_in, self.street_in, self.city_in, self.state_in, self.zip_in))
                line = file.readline().strip()
            
            self.cIndex = 0
            file.close()
        except:
            pass

    def save_file_handler(self):
        """saves addresses into a file with the name entered in the
        filename entry"""
        try:
            file = open(self.filename_var.get(), "w")
            for e in range(len(self.entries)):
                file.write(self.entries[e].name)
                file.write(self.entries[e].street)
                file.write(self.entries[e].city)
                file.write(self.entries[e].state)
                file.write(self.entries[e].zip)
            
            file.close()
        except:
            pass

    def quit_handler(self):
        """quits the program"""
        self.window.destroy()

    def dispNot(self):
        """sets the entries to empty strings"""
        self.name_var.set("")
        self.street_var.set("")
        self.city_var.set("")
        self.state_var.set("")
        self.zip_var.set("")
    
    def setFields(self, entry):
        """sets the entries using the desired address"""
        self.name_var.set(entry.name)
        self.street_var.set(entry.street)
        self.city_var.set(entry.city)
        self.state_var.set(entry.state)
        self.zip_var.set(entry.zip)

    def go(self):
        """ Start the event loop """
        self.window.mainloop()

    # You will add other methods.

def main():
    # Create the GUI program
    program = AddressBook()

    # Start the GUI event loop
    program.go()

if __name__ == "__main__":
    main()   
