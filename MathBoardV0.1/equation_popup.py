"""
Author: Eli lewis
Class: CS 108
Final Project
module description:

Creates the graphing popup
"""

from tkinter import *


class equation_popup:
    def __init__(self, wb):
        self.equation = wb.latest_equation
        self.wb = wb

        self.top = Toplevel()
        self.top.title("Equation")

        self.top.protocol("WM_DELETE_WINDOW", self.quit)

        self.top_frame = Frame(self.top, bg="white")
        self.top_frame.pack(side=TOP, fill=BOTH)
        self.middle_frame = Frame(self.top, bg="white")
        self.middle_frame.pack(side=TOP, fill=BOTH)
        self.bottom_frame = Frame(self.top, bg="white")
        self.bottom_frame.pack(side=TOP, fill=BOTH, expand=True)

        self.canvas = Canvas(self.bottom_frame, bg="white", width=600, height=600)
        self.canvas.pack(expand=True, fill=BOTH)

        Entry(
            self.top_frame,
            textvariable=self.equation.tk_value,
            width=15,
            font=("Arial", 32),
        ).pack(side=LEFT, fill=BOTH, expand=True)

        Button(self.top_frame, text="Done", font=("Arial", 20), command=self.quit).pack(
            side=RIGHT
        )

        Label(self.middle_frame, text="= ", font=("Arial", 32)).pack(side=LEFT)
        Label(
            self.middle_frame, textvariable=self.equation.answer, font=("Arial", 32)
        ).pack(side=LEFT, fill=BOTH, expand=True)

        self.wb.canvas.bind(
            "<ButtonPress-1>", wb.equation
        )  # to move equation button / set
        self.top.bind("<MouseWheel>", self.zoom)  # zoom in and out

        # sets variables needed for drawing graph
        self.top.update_idletasks()
        self.canvas_width = self.top.winfo_width()
        self.width = 10
        self.gap = (self.canvas_width) // self.width

        self.zoom_wait = None  # a queue for zooming

        self.draw_lines()
        self.graph()

    def quit(self):
        self.wb.canvas.bind(
            "<ButtonPress-1>", self.wb.reset
        )  # binds the button press back to reset, the original bind
        self.top.destroy()

    def zoom(self, event):
        """ zooms in or out"""
        self.canvas.delete("grid")
        if event.delta > 0 and self.width > 2:
            self.width -= 2

        elif event.delta < 0 and self.width < 52:
            self.width += 2

        self.gap = (self.canvas_width) // self.width

        if self.zoom_wait:
            self.canvas.after_cancel(self.zoom_wait)

        self.zoom_wait = self.canvas.after(100, self.draw_lines)

    def graph(self):
        """
        Draws the graph below an equation in the popup window
        """
        width = self.width
        gap = self.gap

        # graph the function
        resolution = 10
        self.equation.graph(self.width, resolution)
        self.equation.solve()

        last_x, last_y, = (
            None,
            None,
        )
        self.canvas.delete("graph")

        for P in self.equation.points:
            try:
                x, y = (
                    P[0] + width / 2,
                    (-1 * P[1]) + width / 2,
                )  # translate math coords into canvas coords
                # trims the floats so they dont break tkinter with unreal numbers
                x, y = float("{:.10f}".format(x.real)), float("{:.10f}".format(y.real))

                if last_x and last_y:
                    self.canvas.create_line(
                        last_x * gap,
                        last_y * gap,
                        x * gap,
                        y * gap,
                        fill="Red",
                        width=self.canvas_width / self.width // 5,
                        tag="graph",
                        capstyle=ROUND,
                        smooth=TRUE,
                        splinesteps=36,
                    )
                last_x, last_y, = (
                    x,
                    y,
                )

            except Exception as e:
                pass

        self.canvas.after(500, self.graph)

    def draw_lines(self):
        """
        Draws the graph lines
        """
        width = self.width
        gap = self.gap
        start = 0
        end = self.width * gap

        # x and y intercepts
        self.canvas.create_line(
            (width // 2) * gap, start, (width // 2) * gap, end, tag="grid", width=3
        )
        self.canvas.create_line(
            start, (width // 2) * gap, end, (width // 2) * gap, tag="grid", width=3
        )

        for x in range(width):
            self.canvas.create_window(
                x * gap,
                (width // 2) * gap,
            )
            self.canvas.create_line(x * gap, start, x * gap, end, tag="grid")

            for y in range(width):
                self.canvas.create_line(start, y * gap, end, y * gap, tag="grid")


if __name__ == "__main__":
    """test code for equation_popup """
    pass
