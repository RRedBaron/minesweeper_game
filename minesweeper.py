import tkinter as tk
from tkinter.messagebox import showinfo
from random import shuffle
from button import MyButton

colors = {
    0: 'black',
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

    FIRST_CLICK = True
    GAME_OVER = False
    ROWS = 10
    COLUMNS = 10
    MINES = round(ROWS * COLUMNS * 0.15)

    def __init__(self):
        self.buttons = []
        for i in range(MineSweeper.ROWS + 2):
            temp = []
            for j in range(MineSweeper.COLUMNS + 2):
                btn = MyButton(self.window, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button))
                temp.append(btn)
            self.buttons.append(temp)

    def restart(self):
        [i.destroy() for i in self.window.winfo_children()]
        self.__init__()
        self.create_field()
        MineSweeper.FIRST_CLICK = True
        MineSweeper.GAME_OVER = False

    def breadth_first_search(self, btn: MyButton):
        queue = [btn]
        while queue:
            cur_btn = queue.pop()
            color = colors[cur_btn.amount_of_bombs]
            if cur_btn.amount_of_bombs:
                cur_btn.config(text=cur_btn.amount_of_bombs, disabledforeground=color)
            else:
                cur_btn.config(text='', disabledforeground=color)
            cur_btn.config(state='disabled', relief=tk.SUNKEN)
            cur_btn.is_open = True
            if not cur_btn.amount_of_bombs:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        # if not abs(dy - dx) == 1:
                        # continue
                        next_btn = self.buttons[x + dx][y + dy]
                        if not next_btn.is_open and 1 <= next_btn.x <= MineSweeper.ROWS and \
                                1 <= next_btn.y <= MineSweeper.COLUMNS and next_btn not in queue:
                            queue.append(next_btn)

    def click(self, clicked_btn: MyButton):
        if MineSweeper.GAME_OVER:
            return
        if MineSweeper.FIRST_CLICK:
            MineSweeper.FIRST_CLICK = False
            self.place_mines(clicked_btn.id)
            self.count_mines()
            self.print_buttons()
        if clicked_btn.is_mine:
            clicked_btn.config(text='*', background='red', disabledforeground='black')
            clicked_btn.is_open = True
            MineSweeper.GAME_OVER = True
            showinfo('GAME OVER!', 'Игра окончена!')
            for i in range(1, MineSweeper.ROWS + 1):
                for j in range(1, MineSweeper.COLUMNS + 1):
                    if self.buttons[i][j].is_mine:
                        self.buttons[i][j].config(text='*', disabledforeground='black')
        elif clicked_btn.amount_of_bombs:
            color = colors[clicked_btn.amount_of_bombs]
            clicked_btn.config(text=clicked_btn.amount_of_bombs, disabledforeground=color)
            clicked_btn.is_open = True
        else:
            self.breadth_first_search(clicked_btn)
        clicked_btn.config(state='disabled', relief=tk.SUNKEN)

    def create_field(self):
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label='Start!', command=self.restart)
        settings_menu.add_command(label='Settings')
        settings_menu.add_command(label='Exit', command=MineSweeper.window.destroy)

        menubar.add_cascade(label='Game', menu=settings_menu)

        count = 1
        for i in range(1, MineSweeper.ROWS + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                btn.id = count
                btn.grid(row=i, column=j)
                count += 1

        for i in range(1, MineSweeper.ROWS + 1):
            tk.Misc.grid_rowconfigure(self.window, i, weight=1)
        for i in range(1, MineSweeper.COLUMNS + 1):
            tk.Misc.grid_columnconfigure(self.window, i, weight=1)

    def start_game(self):

        self.create_field()
        MineSweeper.window.mainloop()

    @staticmethod
    def get_indexes(exclude_index: int):
        indexes = list(range(1, MineSweeper.ROWS * MineSweeper.COLUMNS + 1))
        indexes.remove(exclude_index)
        shuffle(indexes)
        return indexes[:MineSweeper.MINES]

    def place_mines(self, excluded_index: int):
        indexes = self.get_indexes(excluded_index)
        for i in range(1, MineSweeper.ROWS + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.id in indexes:
                    btn.is_mine = True

    def count_mines(self):
        for i in range(1, MineSweeper.ROWS + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                count = 0
                btn = self.buttons[i][j]
                for row_dx in [-1, 0, 1]:
                    for col_dy in [-1, 0, 1]:
                        if self.buttons[i + row_dx][j + col_dy].is_mine:
                            count += 1
                btn.amount_of_bombs = count

    def print_buttons(self):
        for i in range(1, MineSweeper.ROWS + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                print(self.buttons[i][j], end='')
            print()
