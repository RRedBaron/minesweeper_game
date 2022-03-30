import tkinter as tk
from random import shuffle
from button import MyButton

colors = {
    1: 'blue',
    2: 'green',
    3: 'red',
    4: 'midnightblue',
    5: 'khaki',
    6: 'pink',
    7: 'brown',
    8: 'violet'
}

class MineSweeper:
    window = tk.Tk()
    window.title("Сапёр")
    window.resizable(width=False, height=False)
    x = (window.winfo_screenwidth() - window.winfo_reqwidth()) / 2
    y = (window.winfo_screenheight() - window.winfo_reqheight()) / 2 - 100
    window.wm_geometry("+%d+%d" % (x, y))

    ROWS = 5
    COLUMNS = 5
    MINES = round(ROWS * COLUMNS * 0.2)

    def __init__(self):
        self.buttons = []
        for i in range(MineSweeper.ROWS+2):
            temp = []
            for j in range(MineSweeper.COLUMNS+2):
                btn = MyButton(self.window, x=i, y=j)
                btn.config(command = lambda button=btn: self.click(button))
                temp.append(btn)
            self.buttons.append(temp)

    def click(self, clicked_btn : MyButton):
        if clicked_btn.is_mine:
            clicked_btn.config(text='*', background='red', disabledforeground='black')
        elif clicked_btn.amount_of_bombs in colors:
            color = colors[clicked_btn.amount_of_bombs]
            clicked_btn.config(text=clicked_btn.amount_of_bombs, disabledforeground=color)
        clicked_btn.config(state='disabled', relief=tk.SUNKEN)

    def create_field(self):
        for i in range(1, MineSweeper.ROWS+1):
            for j in range(1,MineSweeper.COLUMNS+1):
                btn = self.buttons[i][j]
                btn.grid(row = i, column = j)

    def start_game(self):

        self.create_field()
        self.place_mines()
        self.count_mines()
        self.print_buttons()
        self.window.mainloop()

    @staticmethod
    def get_indexes():
        indexes = list(range(1, MineSweeper.ROWS*MineSweeper.COLUMNS+1))
        shuffle(indexes)
        return indexes[:MineSweeper.MINES]

    def place_mines(self):
        indexes = self.get_indexes()
        count = 1
        for i in range(1, MineSweeper.ROWS+1):
            for j in range(1, MineSweeper.COLUMNS+1):
                btn = self.buttons[i][j]
                btn.id = count
                if btn.id in indexes:
                    btn.is_mine = True
                count += 1

    def count_mines(self):
        for i in range(1, MineSweeper.ROWS+1):
            for j in range(1, MineSweeper.COLUMNS+1):
                count = 0
                btn = self.buttons[i][j]
                for row_dx in [-1, 0, 1]:
                    for col_dy in [-1, 0, 1]:
                        if self.buttons[i+row_dx][j+col_dy].is_mine:
                            count+=1
                btn.amount_of_bombs = count

    def print_buttons(self):
        for row in self.buttons:
            print(row)