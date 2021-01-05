"""
Author: Eli lewis
Class: CS 108
Final Project
module description:
creates a class that stores a mathmatical equation as well as methods to solve and / or graph the equation

this is the only class that could be useful on its own
"""

from tkinter import StringVar
from simpleeval import simple_eval
import math, re


class Equation:
    
    def __init__(self, value=""):
        self.tk_value = StringVar()
        self.tk_value.set(value)
        self.answer = StringVar()

        self.points = []

        # set allowed functions to a dictionary of anonymous functions.
        # these are functions that can be accessed when in the graphing module
        self.allowed_functions = {
            "sin": lambda x: math.sin(x),
            "cos": lambda x: math.cos(x),
            "tan": lambda x: math.tan(x),
            "arcsin": lambda x: math.asin(x),
            "arccos": lambda x: math.acos(x),
            "arctan": lambda x: math.atan(x),
            "sqrt": lambda x: math.sqrt(x),
            "abs": lambda x: abs(x),
            "log": lambda x, base=10: math.log(x, base),
        }

    def solve(self):
        """this function uses simple eval to attempt to evaluate the users expression """
        
        #this function is ran in a loop to constantly update the output to be correct.
        #it works on the model that if something executes correctly, its a finished expression:
        #otherwise, its not fully typed or is wrong
        try:
            answer = float(
                simple_eval(
                        self.tk_value.get(),
                        names={"math": math, "pi": math.pi, "e": math.e}, #variables that may be accessed
                        functions=self.allowed_functions
                        )
            )

            self.answer.set("{:.10f}".format(answer))

        except Exception as error:
            pass

    def graph(self, width, resolution):
        """this function uses simple eval to attempt to evaluate the users expression as a function"""

        #this try catches all the errors relating to the function not being fully typed or having a typo etc
        try:
            self.points = []
            
            function = self.tk_value.get()
            function = function.split("=")
            
            
            function_name, function_args, function = (
                
                #match any string that is not 0-9, e, p, i, or ends in (
                re.findall('[^0-9epi(\$]*', function[0])[0], #first instance
                str(re.findall('\([a-z*A-Z*0-9*]*\)', function[0])[0]).strip('()'),
                re.sub(r"((?:\d+)|(?:[a-zA-Z]\w*\(\w+\)))((?:[a-zA-Z]\w*)|\()", r"\1*\2", function[1]) #https://stackoverflow.com/a/35930060
            )
            
            if (re.findall('[0-9epi]',function_args)):
                
                #this try catches all the errors relating to the function not being fully typed or having a typo etc
                try:
                    #TODO: this is inefficient find a better way to do this
                    function_args = simple_eval(
                        function_args,
                        names={"math": math, "pi": math.pi, "e": math.e},
                        functions=self.allowed_functions,
                    )
                    
                    
                    self.answer.set(
                        str(float(simple_eval(
                                        function,
                                         names={'x': function_args, "math": math, "pi": math.pi, "e": math.e},
                                    functions=self.allowed_functions,
                                )))
                        )
                    
                except Exception as e:
                    #print(e)
                    pass
                
                
            else:

                for x in range(
                    -1 * width * resolution // 2, (width * resolution // 2) + 1
                ):
                    #this try is to mainly catch domain errors
                    try:
                        self.points.append([x / resolution])

                        self.points[-1].append(
                            simple_eval(
                                function,
                                names={
                                    function_args: x / resolution,
                                    "math": math,
                                    "pi": math.pi,
                                    "e": math.e,
                                },
                                functions=self.allowed_functions,
                            )
                        )
                    except:
                        pass

        except Exception as error:
            # print(error)
            pass


if __name__ == "__main__":
    """test code for equation """

    # this is needed for stringvar to function
    from tkinter import *

    Tk()

    e = Equation("f(x)=x")
    assert e.tk_value.get() == "f(x)=x"

    e.graph(width=5, resolution=2)

    assert e.points == [
        [-2.5, -2.5],
        [-2.0, -2.0],
        [-1.5, -1.5],
        [-1.0, -1.0],
        [-0.5, -0.5],
        [0.0, 0.0],
        [0.5, 0.5],
        [1.0, 1.0],
        [1.5, 1.5],
        [2.0, 2.0],
        [2.5, 2.5],
    ]

    e.solve()

    try:
        assert e.answer.get() == " "
        raise ValueError(e.answer.get() + " should be " + "")
    except AssertionError:
        pass

    e.tk_value.set("e+1000003232")

    e.solve()

    assert float(e.answer.get()) == "{:.10f}".format(math.e + 1000003232)
