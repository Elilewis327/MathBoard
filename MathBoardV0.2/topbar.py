"""
Author: Eli lewis
Class: CS 108
Final Project
module description:
creates the top menu bar of the program

"""

from tkinter import *
from tkinter import filedialog
import re, equation

class topbar:
    def __init__(self, root, whiteboard):
        self.wb = whiteboard
        self.root = root
        self.Bar()                              

    def Bar(self):
        """
        Draws the top menu bar
        """
        self.file = None

        # menubar docs https://tkdocs.com/tutorial/menus.html
        mainbar = Menu(self.root)
        self.root.config(menu=mainbar)

        pad = "\t\t"
        filemenu = Menu(mainbar, tearoff=0, font=("Arial", 12))
        filemenu.add_command(label="New{}".format(pad), command=self.new)
        filemenu.add_command(label="Open{}".format(pad), command=self._open)
        filemenu.add_command(label="Save{}".format(pad), command=self.save)
        filemenu.add_command(label="Save as{}".format(pad), command=self.save_as)
        filemenu.add_command(label="Exit{}".format(pad), command=self._exit)

        mainbar.add_cascade(label="File ", menu=filemenu)

        editmenu = Menu(mainbar, tearoff=0, font=("Arial", 12))
        editmenu.add_command(label="Clear{}".format(pad), command=self.wb.clear)
        editmenu.add_separator()
        editmenu.add_command(label="Coming Soon!{}".format(pad), command=None)
        editmenu.add_command(label="Undo{}".format(pad), command=None)
        editmenu.add_command(label="Redo{}".format(pad), command=None)
        

        mainbar.add_cascade(label="Edit ", menu=editmenu)

    def _exit(self):
        """
        closes window, asks if you wan to save
        """
        if not self.wb.saved:
            top = Toplevel()
            top.title("Save?")
    
            if not self.file:
                file = "Untitled"
            else:
                file = self.file.rsplit("/", 1)[-1]  # https://stackoverflow.com/a/7253830

            Label(
                top,
                text="Would you like to save {}?".format(file),
                font=("Arial", 15),
                bg="white",
                height=5,
            ).pack(expand=True, fill=BOTH)

            bottom = Frame(top)
            bottom.pack()
            Label(bottom, width=20).pack(side=LEFT, expand=True, fill=BOTH)
            buttons = Frame(bottom)
            buttons.pack(side=RIGHT)
            
            # fix this two function calls in a lambda is undefined behaviour
            Button(
                buttons,
                text="Save",
                bg="#dfe3eb",
                command=lambda: [top.destroy(), self.save()],
                width=10,
                bd="4",
            ).pack(side=LEFT, padx=3, pady=3)
            
            Button(
                buttons,
                text="Don't Save",
                bg="#dfe3eb",
                command=lambda: [top.destroy(), self.root.destroy()],
                width=10,
                bd="4",
            ).pack(side=LEFT, padx=3, pady=3)
            
            Button(
                buttons,
                text="Cancel",
                bg="#dfe3eb",
                command=top.destroy,
                width=10,
                bd="4",
            ).pack(side=LEFT, padx=3, pady=3)
            self.root.wait_window(top) #blocks until save gui skidattles

        else:
            self.root.destroy()
        
        

    def new(self):
        """
        re inits the window. gui doesnt get imported till now to protect against import loops and other shenanigans
        """
        self._exit()
        import gui as Gui
        Gui.gui()

    def save_as(self):
        """
        Gets the file save location
        """
        # get file path
        file_path = filedialog.asksaveasfile(
            initialdir="documents",
            title="Select a save location",
            defaultextension=("wb files", "*.wb"),
            filetypes=(("wb files", "*.wb"), ("all files", "*.*")),
        )
        if file_path:
            self.file = file_path.name
            self.save()

    def _open(self):
        """
        Opens a .wb file for reading
        """
        data = None

        # https://youtu.be/Aim_7fC-inw?t=168
        file_path = filedialog.askopenfilename(
            initialdir="documents",
            title="Select a file",  # title and starting directory
            filetypes=(("wb files", "*.wb"), ("all files", "*.*")),
        )  # filetype options

        # opens the file path gotten from filedialog
        if file_path:
            with open(file_path) as file:
                data = file.readlines()
            self.file = file_path

        # creates the objects in the file on the white board
        if data:
            self.wb.clear()
            for i in data:
                # seperates the line into the "command" and the arguments
                command = re.search('.*\[', i).group().strip('[')

                arguments = re.findall('\[.*\]', i)[0].strip('[]')
                arguments = re.split(',', arguments)
                
                #kwargs get asigned here
                kwargs = {}
                
                for x in arguments:
                    if re.findall('=', x):
                        x = x.split('=')
                        kwargs[x[0]] = x[1]
                
                if command == "line":
                    # asigns width and fill

                    self.wb.canvas.create_line(
                        arguments[0:4],
                        width=kwargs['width'],
                        fill=kwargs['fill'],
                        capstyle=ROUND,
                        tag="drawn_lines",
                    )

                elif command == "textbox":

                    
                    #handle text for textbox's
                    text = kwargs['text']   
                    text = text.replace(
                        "&eq", "=", len(text)
                    )  # replace all instances of %eq with =
                    text = text.replace(
                        "&n", "\n", len(text)
                    )  # replace all instances of  %n with newline
                    text.strip(
                        "&"
                    )  # why is there a extra & at the end of the file? i have no idea. so this is here

                    textbox = Text(
                        self.root,
                        bg="white",
                        fg=kwargs['fg'],
                        width=kwargs['width'],
                        height=kwargs['height'],
                        font=kwargs['font'],
                    )

                    textbox.insert("1.0", text)
                    textbox.lift(aboveThis=self.wb.canvas)

                    self.wb.canvas.create_window(
                        arguments[:2], anchor="nw", window=textbox
                    )

                elif command == "equation":
                    # asigns text and fg
                
                    kwargs['text'] = kwargs['text'].replace(
                        "&eq", "=", len(kwargs['text'])
                    )   

                    # see whiteboard.equation
                    latest_equation = equation.Equation(kwargs['text'])
                    button = Button(
                        self.root,
                        textvariable=latest_equation.tk_value,
                        bg='white',
                        fg=kwargs['fg'],
                        font=kwargs['font'],
                    )

                    Id = self.wb.canvas.create_window(arguments[:2], window=button)

                    button.configure(
                        command=lambda equation=latest_equation, Id=Id: self.wb.redefine_equation(
                            equation, Id
                        )
                    )

    def save(self):
        """
        Saves the contents of the whiteboard into a .wb file
        #TODO: refactor this function, its messy
        """
        wb = self.wb.canvas
        ids = wb.find_all()
        file_data = []

        if not self.file:
            self.save_as()

        for i in ids:
            # if i is a line
            if wb.type(i) == "line":
                coords = wb.coords(i)
                tag = str(wb.gettags(i)).strip("(,)")
                width = wb.itemcget(i, "width")
                fill = wb.itemcget(i, "fill")

                file_data.append(
                    "line[{},width={},fill={},tag={}]\n".format(
                        str(coords).strip("[]"), width, fill, tag
                    )
                )

            # if i is a create_window onject
            elif wb.type(i) == "window":
                coords = wb.coords(i)[
                    :2
                ]  # canvas.create_window only uses the first two numbers
                window = wb.itemcget(i, "window")

                # if the canvas_create objects window is a text window
                if window[:6] == ".!text":
                    # text
                    window = self.root.nametowidget(
                        window
                    )  # this took a long time to find https://stackoverflow.com/a/8895847
                    fg = window.cget("fg")
                    width = window.cget("width")
                    height = window.cget("height")
                    font = window.cget("font")
                    text = window.get("1.0", END)
                    text = text.replace(
                        "=", "&eq", len(text)
                    )  # replace all instances of = with %eq
                    text = text.replace(
                        "\n", "&n", len(text)
                    )  # replace all instances of newline with %n

                    file_data.append(
                        "textbox[{},width={},height={},text={},fg={},font={}]\n".format(
                            str(coords).strip("[]"), width, height, text, fg, font
                        )
                    )

                elif window[:8] == ".!button":
                    window = self.root.nametowidget(
                        window
                    )  # https://stackoverflow.com/a/8895847
                    
                    fg = window.cget("fg")
                    font = window.cget("font")
                    text = window.cget("text")
                    text = text.replace(
                        "=", "&eq", len(text)
                    )  # replace all instances of = with %eq
                    
                    command = window.cget("command")

                    file_data.append(
                        "equation[{},text={},fg={},font={}]\n".format(
                            str(coords).strip("[]"), text, fg, font
                        )
                    )

        if self.file: #checks to see if file exists: this can still equal None if they hit cancel on the file selection box
            with open(self.file, "w") as file:
                file.writelines(file_data)

            self.wb.saved = True
