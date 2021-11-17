import tkinter
from tkinter import ttk
from pickle import load
from os.path import exists
from db import SimpleDB


class ThemeMother:
    """
    Every Theme in app should inherit from this class, the can define their own type of widgets bellow.
    """
    name = ""  # name of theme that will be showed to user
    Tk = tkinter.Tk
    Toplevel = tkinter.Toplevel
    Button = tkinter.Button
    Label = tkinter.Label
    Frame = tkinter.Frame
    Entry = tkinter.Entry
    Treeview = ttk.Treeview


class DefaultTheme(ThemeMother):
    name = "Default"

    class Tk(ThemeMother.Tk):
        def __init__(self):
            super(ThemeMother.Tk, self).__init__()
            self.config(bg="white")

    class Toplevel(ThemeMother.Toplevel):
        def __init__(self, master):
            super(ThemeMother.Toplevel, self).__init__(master)
            self.config(bg="white")


# After all themes has defined:
if exists("db_class.bin"):
    with open("db_class.bin", "rb") as f:
        Db = load(f)
else:
    Db = SimpleDB
appdata = Db()
if "Theme" in appdata:
    Theme = appdata["Theme"]
else:
    Theme = DefaultTheme


class AskString(Theme.Toplevel):
    def __init__(self, master, message: str = "", title: str = "Input"):
        super(Theme.Toplevel, self).__init__(master)
        self._res = ""
        self.title(title)
        self.columnconfigure(1, weight=1)
        Theme.Label(self, text=message).grid(row=1, column=1, pady=5)
        self._ent = Theme.Entry(self, width=40)
        self._ent.grid(row=2, column=1, pady=8)
        Theme.Button(self, text="Okay", command=self._okay).grid(row=3, column=1, pady=5)
        self.bind("<Enter>", lambda e: self._okay())

    def _okay(self):
        self._res = self._ent.get()
        self.destroy()

    def get_answer(self):
        self.winfo_ismapped() and self.wait_window()
        return self._res


class UserPanel(Theme.Tk):
    pass
