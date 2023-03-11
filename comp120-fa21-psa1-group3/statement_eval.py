# File: statement_eval.py
# Author: Long Pham and Scott Schnieders 
# Date: 9/23/21
# Description: Program that reads and interprets a
#    file containing simple expression and assignment
#    statements.

import re

class BadStatement(Exception):
    pass


def isValidVarStatement(str):
    """
    Function that takes a string and determines if it is 
    a variable. It returns a boolean, true if it is a variable name 
    and false if it is a number. Raises Badstatement if the string 
    parameter doesn't match a variable name or number
    """
    if len(str) >= 3 and str[1] == "=":
        match = re.fullmatch("[a-zA-Z_][a-zA-Z0-9_]*", str[0])
        if match == None:
            raise BadStatement
    elif len(str) < 3 and "=" in str:
        raise BadStatement

def interpret_statements(filename): # interpret file lines
    """
    Function that reads statements from the file whose
    name is filename, and prints the result of each statement,
    formatted exactly as described in the psa1 problem statement.  
    interpret_statements must use the evaluate_expression function,
    which appears next in this file.
    """
    try:
        f = open(filename)
    except FileNotFoundError:
        print("File could not be found or opened.")
        return
    lines = list()
    vars = dict()
    line_count = 0
    for line in f:
        line_count += 1

        if "#" in line: #gets rid of comments
            l = (line.split("#")[0]).strip()
        else:
            l = line.strip()

        if len(l) > 0:
            vals = l.split()
            try:
                print("Line", line_count, end="")
                isValidVarStatement(vals)
                if len(vals) >= 3 and vals[1] == "=":
                    vars[vals[0]] = evaluate_expression(vals[2:], vars) #set the variable to the expression value
                    print(":", f"{vals[0]} = {vars[vals[0]]:.2f}")
                else:
                    value = evaluate_expression(vals, vars) #get the value of a plain expression
                    print(":", f"{l} = {value:.2f}")
            except BadStatement:
                print(": Invalid statement")
                
def evaluate_expression(tokens, variables): # evaluate statements
    """
    Function that evaluates an expression represented by tokens.
    tokens is a list of strings that are the tokens of the expression.  
    For example, if the expression is "salary + time - 150", then tokens would be
    ["salary", "+", "time", "-", "150"].  variables is a dictionary that maps 
    previously assigned variables to their floating point values.

    Returns the value that is assigned.

    If the expression is invalid, the BadStatement exception is raised.
    """
    try:
        if len(tokens) % 2 == 0: #check for uneven statements
            raise BadStatement
        
        if tokens[0] in variables: #gets the initial number
            final_sum = float(variables[tokens[0]])
        else:
            final_sum = float(tokens[0])

        for i in range(2, len(tokens), 2): #loops throughout to sum the equation
            if tokens[i] in variables:
                num_token = float(variables[tokens[i]])
            else:
                num_token = float(tokens[i])
            
            if tokens[i - 1] == "+":
                final_sum = final_sum + num_token
            elif tokens[i - 1] == "-":
                final_sum = final_sum - num_token
            else:
                raise BadStatement
            
        return final_sum
    except:
        raise BadStatement
        
# You can add additional helper method(s) if you want.

if __name__ == "__main__":
    file_name = "statements.txt"  # you can create another file with statements
                                  # and change the name of this variable to that
                                  # filename.
    
    interpret_statements(file_name)
