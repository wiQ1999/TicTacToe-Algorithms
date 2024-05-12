from tkinter import *
from tkinter import messagebox
from environments.base_game_env import BaseGameEnv
from environments.game_state_enum import GameState

class FormApplication:
    _info_font = ('Arial', 12)
    _board_font = ('Arial', 30)

    def __init__(self):
        self._game = BaseGameEnv()
        self._root = Tk()
        self._root.title("Tic Tac Toe")
        self._player_x_label = Label()
        self._player_y_label = Label()
        self._status_lable = Label()
        self._create_info_section()
        self._buttons = []
        self._create_board_section()
        self._root.resizable(False, False)

    def _create_info_section(self):
        info = Frame(self._root)
        info.pack(side=TOP, fill=X, expand=True)
        player_x = Frame(info)
        player_x.grid(row=0, column=0)
        player_x.grid_rowconfigure(0, minsize=50)
        player_x.grid_columnconfigure(0, minsize=150)
        Label(player_x, text="Player X", font=self._info_font).grid(row=0)
        self._player_x_label = Label(player_x, text="Human", font=self._info_font)
        self._player_x_label.grid(row=1)
        status = Frame(info)
        status.grid(row=0, column=1)
        status.grid_rowconfigure(0, minsize=50)
        status.grid_columnconfigure(0, minsize=150)
        Label(status, text="Status:", font=self._info_font).grid(row=0)
        self._status_lable = Label(status, font=self._info_font)
        self._status_lable.grid(row=1)
        Button(status, text='Resetuj', font=self._info_font, command=lambda: self.restart_game()).grid(row=1)
        player_y = Frame(info)
        player_y.grid(row=0, column=2)
        player_y.grid_rowconfigure(0, minsize=50)
        player_y.grid_columnconfigure(0, minsize=150)
        Label(player_y, text="Player O", font=self._info_font).grid(row=0)
        self._player_y_label = Label(player_y, text="Human", font=self._info_font)
        self._player_y_label.grid(row=1)

    def _create_board_section(self):
        board = Frame(self._root)
        board.pack(side=BOTTOM, fill=BOTH, expand=True)
        for x in range(3):
            row = []
            for y in range(3):
                pos = Button(board, text='', font=self._board_font, command=lambda ix=x, iy=y: self._set_position(ix, iy))
                pos.grid(row=x, column=y, sticky="nsew")
                board.grid_columnconfigure(x, minsize=150)
                board.grid_rowconfigure(y, minsize=150)
                row.append(pos)
            self._buttons.append(row)

    def _switch_positions(self, activity: bool):
        button_state = ACTIVE if activity else DISABLED
        for x in range(3):
            for y in range(3):
                self._buttons[x][y].config(state=button_state)

    def _set_position(self, x: int, y: int):
        if self._game.is_position_taken(x, y):
            return
        symbol = self._game.current_player.symbol
        self._game.move(x, y)
        self._buttons[x][y].config(text=symbol)
        if self._game.game_state == GameState.PLAYING:
            return
        elif self._game.game_state == GameState.DRAW:
            self._switch_positions(False)
            messagebox.showinfo("Game Over", "It's a draw!")
        else:
            self._switch_positions(False)
            messagebox.showinfo("Game Over", f"Player {symbol} wins!")

    def run(self):
        self._root.mainloop()

    def restart_game(self):
        self._game.restart()
        self._switch_positions(True)
        for x in range(3):
            for y in range(3):
                self._buttons[x][y].config(text='')