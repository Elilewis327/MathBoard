"""
Author: Eli lewis
Class: CS 108
Final Project
module description:
creates the whiteboard section of the gui.
when ran on its own creates a very simple whiteboard with no buttons.
"""

from tkinter import *
from equation_popup import equation_popup


class whiteboard:
    def __init__(self, window, width="1062", height="600"):

        self.width, self.height = width, height
        self.window = window  # root window

        self.canvas = Canvas(
            self.window, width=self.width, height=self.height, bg="white"
        )
        self.canvas.pack(fill=BOTH, expand=True, pady=0, padx=10)

        self.pen = pen()
        self.reset()

        self.bind()

        self.saved = True

        self.focal_x, self.focal_y, = (0, 0,)  # how left or right the view is
        self.zoom_level = 0  # how zoomed in or out the view is

    def bind(self):
        """
        This function initializes or unbinds button binds. True to bind, false to unbind.
        """
        # canvas binds
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.reset)
        self.canvas.bind("<ButtonPress-1>", self.reset)

        # canvas zoom and scroll binds
        self.window.bind("<MouseWheel>", self.zoom)
        self.canvas.bind("<B3-Motion>", self.change_focus)
        self.canvas.bind("<ButtonPress-3>", self.mark_focus)
        self.canvas.bind("<ButtonRelease-3>", self.final_focus)

    """Focus related methods"""

    def mark_focus(self, event):
        """
        Sets a "mark" where the canvas is clicked for the dragto method
        """
        self.mark_event = event
        self.canvas.scan_mark(event.x, event.y)  # sets an initial mark on the canvas

    def change_focus(self, event):
        """
        sets the end mark for where the canvas is dragged to
        """
        self.canvas.scan_dragto( event.x, event.y, gain=1)  # translates the canvas. gain is a multiplier to the other values.

    def final_focus(self, event):
        """
        computes the offset so drawing is under the mouse after translation
        """
        self.focal_x += event.x - (self.mark_event.x)
        self.focal_y += event.y - self.mark_event.y

    """zoom related methods"""

    def zoom(self, event):
        """ zooms in or out with the mouse wheel"""

        # code that accounts for leftword or rightword focus changes
        x, y = event.x - self.focal_x, event.y - self.focal_y

        if event.delta > 0 and self.zoom_level < 15:  # delta is for the scroll wheel
            self.zoom_level += 1
            scale_factor = 1.1

        elif event.delta < 0 and self.zoom_level > -15:
            self.zoom_level -= 1
            scale_factor = 0.9

        else:
            scale_factor = 1.0

        # scales all the objects on the canvas larger or smaller
        self.canvas.scale(ALL, x, y, scale_factor, scale_factor)

    def reset_view(self):
        """A function that sets the x/y translation to default"""

        # https://stackoverflow.com/a/40595132
        self.canvas.xview_moveto(0.0)
        self.canvas.yview_moveto(0.0)

        self.focal_x, self.focal_y = 0, 0

        if self.zoom_level < 0:
            scale_factor = 1.1

        elif self.zoom_level > 0:
            scale_factor = 0.9

        for i in range(abs(self.zoom_level)):

            self.canvas.scale(
                ALL,
                int(self.width) / 2,
                int(self.height) / 2,
                scale_factor,
                scale_factor,
            )

        self.zoom_level = 0

    """drawing/ erasing methods"""

    def draw(self, event):
        """ main code for drawing lines on the whiteboard"""
        # code that accounts for leftword or rightword focus changes
        x, y = event.x - self.focal_x, event.y - self.focal_y

        if self.old_x and self.old_y:
            self.canvas.create_line(
                self.old_x, self.old_y,
                x, y,  # creates a line between the last x and y to the latest x and y
                width=self.line_width.get(),
                fill=self.color,  # sets the width of the line and its color
                capstyle=ROUND,
                tag="drawn_lines",
            )  # round capstyle makes the lines look less sharp

        self.old_x = x
        self.old_y = y

    def reset(self, event=""):
        """
        this function is called at the start and end of each line.
        it's called at the start to ensure the correct width and color
        it's called at the end to reset the variables
        """

        self.old_x, self.old_y = None, None
        self.line_width = self.pen.width
        self.color = self.pen.color
        self.eraser_width = 0  # resets the eraser width
        self.canvas.delete(
            "erase"
        )  # anything with the tag erase is deleted. the erase tag is added by the eraser
        self.saved = False

    def clear(self):
        """ clears the canvas """
        self.canvas.delete(ALL)

    def eraser_enable(self):
        """function for enabling erasing"""
        self.canvas.bind("<B1-Motion>", self.erase)

    def eraser_disable(self):
        """function for disabling erasing"""
        self.canvas.bind("<B1-Motion>", self.draw)

    def erase(self, event):
        """ eraser """
        # code that accounts for leftword or rightword focus changes
        x, y = event.x - self.focal_x, event.y - self.focal_y

        if self.old_x and self.old_y:

            # the eraser grows as you hold the button down
            if self.eraser_width < 100:
                self.eraser_width += 1

            # anything with the erase tag is removed
            self.canvas.delete("erase")
            radius = self.eraser_width / 2

            radius_offset = ((radius)*(2)**(1/2))/2  # this is the side length of the largest possible square in the circle

            # anything that touches the square created below gets the erase tag
            self.canvas.addtag_overlapping(
                "erase",
                x - radius_offset,
                y - radius_offset,
                x + radius_offset,
                y + radius_offset,
            )

            # visualizes exactly where the erasing part is
            """self.canvas.create_rectangle(x-radius_offset, y-radius_offset,
                                       x+radius_offset, y+radius_offset, tag='erase')
            """

            # creates a oval that visualizes about where the eraser is
            self.canvas.create_oval(
                x - radius, y - radius,
                x + radius, y + radius,
                tag="erase"
            )

        self.old_x = x
        self.old_y = y

    """equation and graphing code"""

    def equation(self, event=""):
        """
        Gets the postion the button will be pressed from event
        draws the button ad solves for it
        """
        if event:
            # code that accounts for leftword or rightword focus changes
            x, y = event.x - self.focal_x, event.y - self.focal_y

            # defines button for canvas
            button = Button(
                self.window,
                textvariable=self.latest_equation.tk_value,
                bg="white",
                fg=self.pen.color,
                font=(("Arial", self.pen.font_size.get())),
            )

            # creates a button on the canvas where you click
            Id = self.canvas.create_window(x, y, window=button)

            # makes clicking the button call redefine equation; Id is needed to remove the old equation button so a new one can be placed
            button.configure(
                command=lambda equation=self.latest_equation, Id=Id: self.redefine_equation(
                    equation, Id
                )
            )

            self.latest_equation.solve()

            self.canvas.bind("<ButtonPress-1>", self.reset)

    def redefine_equation(self, equation, Id):
        """
        this is called by clicking on a already defined equation.
        Args: equation instance, canvas Id
        """

        self.latest_equation = equation
        self.canvas.delete(Id)

        equation_popup(self)

    def new_textbox_start(self, event):
        """
        Sets the start point for a new text box on the canvas.
        called once on click of m1 after text button is clicked
        """
        # code that accounts for leftword or rightword focus changes
        x, y = event.x - self.focal_x, event.y - self.focal_y

        self.text_box_anchor = (x, y)
        self.canvas.bind("<ButtonPress-1>", self.reset)

    """textbox code """

    def new_textbox_change(self, event):
        """
        Sets the end point for a new text box on the canvas.
        called many times as mouse is moved
        """
        # code that accounts for leftword or rightword focus changes
        x, y = event.x - self.focal_x, event.y - self.focal_y

        self.canvas.delete("tbox-temp")

        width = (
            x - self.text_box_anchor[0]
        )  # the distance between the current point and the initial point
        height = y - self.text_box_anchor[1]

        f_size = int(self.pen.font_size.get())
        textbox = Text(
            self.window,
            bg="white",
            fg=self.pen.color,
            width=width // f_size,  # width is the width divided by the font size
            height=height // f_size,
            font=("Arial", f_size),
        )

        textbox.lift(
            aboveThis=self.canvas
        )  # lower the textbox to be 1 layer above the canvas

        self.canvas.create_window(
            self.text_box_anchor[0],
            self.text_box_anchor[1],
            window=textbox,
            anchor=NW,
            tag="tbox-temp",
        )  # tag for erasing "in between" textboxs

    def new_textbox_end(self, event):
        """
        removes the temp tag from the textbox, so a new one can be created
        called once on release of m1
        """
        self.canvas.dtag(
            "tbox-temp"
        )  # removes the tag tbox-temp from the last text box
        self.text_box_anchor = None

        self.canvas.bind("<B1-Motion>", self.draw)  # resets all the binds
        self.canvas.bind("<ButtonRelease-1>", self.reset)


class pen:
    """A class that stores all the atributes related to the pen """

    def __init__(self, size=5, color="#000000", font_size=32):
        self.color = color
        self.width = StringVar()
        self.width.set(size)
        self.font_size = StringVar()
        self.font_size.set(font_size)


if __name__ == "__main__":
    # just the whiteboard portion of the canvas
    root = Tk()
    wb = whiteboard(root)
    root.mainloop()
