"""
Author: Eli lewis
Class: CS 108
Final Project
module description:
main gui class for final project
creates the top bar and draws the canvas.

Please run this on windows. It does not function correctly on macos.
"""

from tkinter import *
from whiteboard import whiteboard
from equation_popup import equation_popup
from sub_windows import *
from topbar import *
from iconb64 import icon


class gui:
    """
    Creates the final project
    """

    def __init__(self):

        # class inits
        self.root = Tk()
        self.root.title("Mathboard")

        # set icon
        self.root.iconphoto(True, PhotoImage(data=icon))  # the true makes it go down to sub windows

        # frame at the top for buttons
        self.button_frame = Frame(self.root, bg="white")
        self.button_frame.pack(
            fill=BOTH,  # fill all assigned space on the x and y axis'
            expand=False,  # give no additional extra screen space to the frame
            pady=(0, 10),
        )

        self.wb = whiteboard(self.root)
        self.Draw_Buttons()
        self.topbar = topbar(self.root, self.wb)  # inits the very topbar of the gui

        self.button_frame.lift(
            aboveThis=self.wb.canvas
        )  # assures the top bar is always items on the canvas

        self.root.protocol(
            "WM_DELETE_WINDOW", self.topbar._exit
        )  # makes x call the correct exit function

        self.root.mainloop()

    def Draw_Buttons(self):
        """
        A function that draws the buttons in the top bar of the gui
        """

        # font for all the buttons
        button_font = ("Arial", 12)

        # Color button
        # All other buttons in this function are based off this one.
        self.color_button = Button(
            self.button_frame,
            text="Current\nColor",
            bd="4",  # the border width
            fg="white",  # foreground color
            width=6,
            height=2,
            command=self.Change_Color,  # the callback function for this button
            bg=self.wb.pen.color,  # the background color
            font=button_font)  # the font used for the text



        self.color_button.pack(
            side=LEFT, pady=5, padx=5)  # the button goes as far left as possible and has a 5u gap on each side

        # quick select color buttons
        # these are buttons to select common colors without having to open the color changer interface
        self.quick_select_colors = {
            "Black": Button(self.button_frame, width=5, height=2, bg="#000000", bd="0"),
            "Red": Button(self.button_frame, width=5, height=2, bg="#ff0000", bd="0"),
            "Green": Button(self.button_frame, width=5, height=2, bg="#00aa00", bd="0"),
            "Blue": Button(self.button_frame, width=5, height=2, bg="#0000ff", bd="0"),
        }

        for i in self.quick_select_colors:

            self.quick_select_colors[i].configure(
                font=button_font,
                # lambda for corrent arguments, color is the same as the current background color
                command=lambda color=self.quick_select_colors[i]["bg"]: self.Change_Color_Quick(color))

            # this packs all the color quick selects
            self.quick_select_colors[i].pack(side=LEFT, padx=1)

        # Width button
        self.width_button = Button(
            self.button_frame,
            text="Width",
            bd="4",
            width=6,
            height=2,
            font=button_font,
            command=self.Change_Width,
        )
        
        self.width_button.pack(side=LEFT, pady=10, padx=10)

        # current width label
        self.show_width = Entry(
            self.button_frame,
            width=2,
            bd="4",
            bg="#FFFFFF",
            textvariable=self.wb.pen.width,
            font=("Arial", self.wb.pen.font_size.get()),
        )
        
        self.show_width.pack(side=LEFT)

        # Text button
        self.text_button = Button(
            self.button_frame,
            text="Text",
            bd="4",
            width=6,
            height=2,
            font=button_font,
            command=self.New_Textbox,
        )
        
        self.text_button.pack(side=LEFT, pady=10, padx=10)

        # current font label
        self.show_font = Entry(
            self.button_frame,
            width=2,
            bd="4",
            textvariable=self.wb.pen.font_size,
            font=("Arial", self.wb.pen.font_size.get()),
        )
        
        self.show_font.pack(side=LEFT, pady=10, padx=10)

        # Equation button
        self.equation_button = Button(
            self.button_frame,
            text="Equation",
            bd="4",
            width=12,
            height=2,
            font=button_font,
            command=self.New_Equation,
        )
        
        self.equation_button.pack(side=LEFT, pady=10, padx=10, fill=X)

        # Clear button
        self.clear_button = Button(
            self.button_frame,
            text="Clear",
            bd="4",
            width=10,
            height=2,
            font=button_font,
            command=self.wb.clear,
        )
        
        self.clear_button.pack(side=RIGHT, pady=10, padx=10)

        # Erase button
        self.erase_button = Button(
            self.button_frame,
            text="Erase",
            bd="4",
            width=8,
            height=2,
            font=button_font,
            command=self.wb.eraser_enable,
        )
        
        self.erase_button.pack(side=RIGHT, pady=10, padx=10)

        # button that resets the viewfinder
        self.reset_view_button = Button(
            self.button_frame,
            text="Reset View",
            bd="4",
            width=10,
            height=2,
            font=button_font,
            command=self.wb.reset_view,
        )
        
        self.reset_view_button.pack(side=RIGHT, pady=10, padx=10)

    def New_Equation(self):
        """
        When the equation button is clicked this function is called.
        """
        self.wb.latest_equation = None
        equation_popup(self.wb)  # new equation popup

    def New_Textbox(self):
        """
        Binds m1 to create a new text box
        """
        self.wb.canvas.bind("<ButtonPress-1>", self.wb.new_textbox_start)
        self.wb.canvas.bind("<B1-Motion>", self.wb.new_textbox_change)
        self.wb.canvas.bind("<ButtonRelease-1>", self.wb.new_textbox_end)

    def Change_Color_Quick(self, color):
        """
        changes the quickselect colors
        Args: color, must be hex
        """
        if (
            str(color)[0] == "#"
        ):  # checks for hexcode hashtag, else raises a value error
            self.wb.pen.color = color  # set the whiteboard 'pen' to the new color
            
            self.color_button.configure(
                bg=color
            )  # update the color button to the new selected color
            
            self.wb.eraser_disable()  # makes sure the pen is active
        else:
            raise ValueError("Argument 'color' must be a hex color code.")

    def Change_Color(self):
        """
        -Called By color_button
        -Inits select color child window
        -Args: None
        """
        sc = Select_Color(self.wb.pen.color)  # color popup window
        self.color_button.configure(
            state=DISABLED
        )  # disable button while popup is open
        self.root.wait_window(sc.top)  # waits for popup to be destroyed
        self.wb.pen.color = sc.new_color  # sets pen to new color
        
        self.color_button.configure(
            state=NORMAL, bg=sc.new_color
        )  # re enable button after pop up is closed
        
        self.wb.eraser_disable()  # makes sure the pen is active

    def Change_Width(self):
        """
        -Called By width_button
        -Inits select width child window
        -Args: None
        """
        sw = Select_Width(self.wb.pen.width.get())  # change width popup
        
        self.width_button.configure(
            state=DISABLED
        )  # disable button while popup is open
        
        self.root.wait_window(sw.top)  # waits for popup to be destroyed
        self.wb.pen.width.set(sw.new_width)  # sets pen to new width
        
        self.width_button.configure(
            state=NORMAL
        )  # re enable button after pop up is closed
        
        self.wb.eraser_disable()  # makes sure the pen is active

if __name__ == "__main__":
    gui()  # calls the gui class
