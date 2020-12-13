"""
Author: Eli lewis
Class: CS 108
Final Project
module description:
creates a class that stores a tkinter StringVar and a method to solve whats in the StringVar
"""

from tkinter import StringVar
from simpleeval import simple_eval
import math

class Equation():
    
    def __init__(self, value=''):
        self.tk_value = StringVar()
        self.tk_value.set(value)
        self.answer = StringVar()
        
        self.points = []
        
        #set allowed functions to a dictionary of anonymous functions.
        #these are functions that can be accessed when in the graphing module
        self.allowed_functions = {'sin': lambda x: math.sin(x), 'cos': lambda x: math.cos(x),
                                  'tan': lambda x: math.tan(x), 'arcsin': lambda x: math.asin(x),
                                   'arccos': lambda x: math.acos(x),'arctan': lambda x: math.atan(x),
                                   'sqrt': lambda x: math.sqrt(x), 'abs': lambda x: abs(x),
                                   'log': lambda x, base=10: math.log(x, base)}
        
    def solve(self):
        """this function uses simple eval to attempt to evaluate the users expression """
        try:
            answer = float(simple_eval(self.tk_value.get(), names={'math': math, 'pi': math.pi, 'e':math.e},
                                 functions=self.allowed_functions))
            
            self.answer.set("{:.10f}".format(answer))
        
        except Exception as error:
            #print(error)
            pass
            
    def graph(self, width, resolution):
        """this function uses simple eval to attempt to evaluate the users expression as a function"""
        try:
            self.points = []
            function = self.tk_value.get()
            function = function.split('=')
            if function[0][0].isalpha() and function[0][1] == '(':
                function_name, function_args, function = function[0][0], function[0][1:].strip("()"), function[1]
                self.tk_value.set((str(function_name) + '(' + str(function_args) + ')' + '=' + str(function)))
                
                if function_args.isnumeric() or function_args == 'pi' or function_args == 'e':
                    function_args = simple_eval(function_args, names={'math': math, 'pi':math.pi,'e':math.e},
                                                      functions=self.allowed_functions)
                    self.answer.set(str(float(simple_eval(function, names={'x': function_args, 'math': math, 'pi':math.pi,'e':math.e},
                                                      functions=self.allowed_functions))))
                else:

                    for x in range(-1*width*resolution//2, (width*resolution//2)+1):
                        try:
                            self.points.append([x/resolution])
                
                            self.points[-1].append(simple_eval(function, names={function_args: x/resolution, 'math': math, 'pi':math.pi, 'e':math.e},
                                                   functions=self.allowed_functions))
                        except:
                            pass
                        
        except Exception as error:
            #print(error)
            pass
        
if __name__ == '__main__':
    """test code for equation """
    from tkinter import *
    
    def solve():
        equation.graph()
        root.after(1000, solve)
    
    root = Tk()
    equation = Equation()
    Entry(root, textvariable=equation.tk_value, font=('Arial', 32)).pack()
    Label(root, textvariable=equation.tk_value, font=('Arial', 32)).pack()
    solve()
    
