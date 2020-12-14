"""
Author: Eli lewis
Class: CS 108
Final Project
module description:
creates  multiple subwindow classes that are called when their respective buttons are pressed
"""

from tkinter import *


class SubWindow:
    def __init__(self, Title):
        """ this class provides a base class for all child windows of gui"""
        self.top = Toplevel()
        self.top.title(Title)


class Select_Color(SubWindow):
    """
    This class provides a child window color selector
    """

    def __init__(self, current_color):

        super().__init__("Select a Color")

        self.current_color = current_color
        self.rgb = self.hex_to_rgb()
        self.draw()

    def draw(self):
        """
        This draws the gui in the select color window
        """
        for i in self.top.winfo_children():
            # if the draw function is called after __init__, this loop clears the gui for redrawing
            # this happens when the show_current_color button is clicked
            i.destroy()

        upper_frame = Frame(self.top)
        upper_frame.pack()
        slider_frame = Frame(upper_frame)
        slider_frame.pack(side=LEFT)

        # red fader
        Label(slider_frame, text="Red").grid(row=0, column=0)
        self.R = Scale(
            slider_frame, from_=0, to=255, orient=HORIZONTAL, length=500, showvalue=True
        )
        self.R.grid(row=0, column=1)
        self.R.set(self.rgb[0])  # this sets the fader to the current color value

        # green fader
        Label(slider_frame, text="Green").grid(row=1, column=0)
        self.G = Scale(
            slider_frame, from_=0, to=255, orient=HORIZONTAL, length=500, showvalue=True
        )
        self.G.grid(row=1, column=1)
        self.G.set(self.rgb[1])  # this sets the fader to the current color value

        # blue fader
        Label(slider_frame, text="Blue").grid(row=2, column=0)
        self.B = Scale(
            slider_frame, from_=0, to=255, orient=HORIZONTAL, length=500, showvalue=True
        )
        self.B.grid(row=2, column=1)
        self.B.set(self.rgb[2])  # this sets the fader to the current color value

        # this is a button on the right side of the gui that resets the change color window to what it was on __init__
        self.show_current_color = Button(
            upper_frame,
            height=5,
            width=10,
            bd="4",
            fg="white",
            bg=self.current_color,
            text="Last Color",
            command=self.draw,
        )

        self.show_current_color.pack(fill=BOTH, expand=True, padx=3, pady=3, side=RIGHT)

        # shows the hex value in the color slider of what the current color is
        self.show_color = Label(self.top, width=10, fg="white")
        self.show_color.pack(fill=BOTH, expand=True)
        self.get_vals()

    def get_vals(self):
        """
        this function gets the color from the sliders and changes it to hex (its in rgb originally)
        """
        self.new_color = "#%02x%02x%02x" % (
            self.R.get(),
            self.G.get(),
            self.B.get(),
        )  # this line is from https://stackoverflow.com/a/3380739
        # turns the widget at the bottom of the gui the current color shown on the slider
        self.show_color.configure(bg=self.new_color, text=self.new_color)
        self.top.after(100, self.get_vals)

    def hex_to_rgb(self):
        """
        This function is from https://gist.github.com/matthewkremer/3295567
        """
        hex_ = self.current_color.lstrip("#")
        hlen = len(hex_)
        return tuple(
            int(hex_[i : i + hlen // 3], 16) for i in range(0, hlen, hlen // 3)
        )


class Select_Width(SubWindow):
    def __init__(self, current_width):

        super().__init__("Select a Width")

        Label(self.top, text="Width").pack()
        self.width_slider = Scale(
            self.top, from_=0, to=50, orient=HORIZONTAL, length=500, showvalue=True
        )
        self.width_slider.pack()
        self.width_slider.set(current_width)
        self.get_vals()

    def get_vals(self):
        self.new_width = self.width_slider.get()
        self.top.after(100, self.get_vals)
