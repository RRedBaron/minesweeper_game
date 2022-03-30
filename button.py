import tkinter as tk


class MyButton(tk.Button):
    def __init__(self, master, x, y, index=0, *args, **kwargs):
        super(MyButton, self).__init__(master, width=3, font="Calibri 15 bold",  *args, **kwargs)
        self.x = x
        self.y = y
        self.id = index
        self.is_mine = False
        self.amount_of_bombs = 0
        self.is_open = False

    def __str__(self):
        return f"{self.amount_of_bombs if not self.is_mine else 'B'}"