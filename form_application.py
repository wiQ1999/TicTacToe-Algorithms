from tkinter import *
from environments.ui_game_env import UiGameEnv
from typing import List

class FormApplication:
    _info_font = ('Arial', 12)
    _board_font = ('Arial', 30)

    def __init__(self):
        self._game = UiGameEnv()
        self._root = Tk()
        self._root.title('Tic Tac Toe')
        self._buttons: List[List[Button]] = []
        self._create_info_section()
        self._create_board_section()
        self._root.resizable(False, False)

    def _create_info_section(self):
        info = Frame(self._root)
        info.pack(side=TOP, fill=X, expand=True)
        player_x_frame = Frame(info)
        player_x_frame.grid(row=0, column=0)
        player_x_frame.grid_rowconfigure(0, minsize=50)
        player_x_frame.grid_columnconfigure(0, minsize=150)
        Label(player_x_frame, text='Player X', font=self._info_font).grid(row=0)
        player_x_str = StringVar(player_x_frame, self._game.player_x)
        player_x_cbox = OptionMenu(player_x_frame, player_x_str, *self._game.available_players, command=lambda name: self._player_on_select(name, True))
        player_x_cbox.grid(row=1)
        state_frame = Frame(info)
        state_frame.grid(row=0, column=1)
        state_frame.grid_rowconfigure(0, minsize=50)
        state_frame.grid_columnconfigure(0, minsize=150)
        self._state_lable = Label(state_frame, text=f'State: {self._game.state}', font=self._info_font)
        self._state_lable.grid(row=0)
        Button(state_frame, text='Resetuj', font=self._info_font, command=self._restart_on_click).grid(row=1)
        player_o_frame = Frame(info)
        player_o_frame.grid(row=0, column=2)
        player_o_frame.grid_rowconfigure(0, minsize=50)
        player_o_frame.grid_columnconfigure(0, minsize=150)
        Label(player_o_frame, text='Player O', font=self._info_font).grid(row=0)
        player_o_str = StringVar(player_o_frame, self._game.player_o)
        self._player_o_cbox = OptionMenu(player_o_frame, player_o_str, *self._game.available_players, command=lambda name: self._player_on_select(name, False))
        self._player_o_cbox.grid(row=1)

    def _player_on_select(self, name: StringVar, is_x: bool):
        if is_x:
            self._game.player_x = name
        else:
            self._game.player_o = name
        self._update_view()

    def _restart_on_click(self):
        self._game.restart()
        self._update_view()

    def _create_board_section(self):
        board = Frame(self._root)
        board.pack(side=BOTTOM, fill=BOTH, expand=True)
        for x in range(3):
            row = []
            for y in range(3):
                pos = Button(board, text='', 
                             font=self._board_font, 
                             command=lambda ix=x, iy=y: self._position_on_click(ix, iy))
                pos.grid(row=x, column=y, sticky="nsew")
                board.grid_columnconfigure(x, minsize=150)
                board.grid_rowconfigure(y, minsize=150)
                row.append(pos)
            self._buttons.append(row)

    def _position_on_click(self, x: int, y: int):
        is_moved = self._game.manual_move(x, y)
        if is_moved:
            self._update_view()

    def _update_view(self):
        self._state_lable.configure(text=f'State: {self._game.state}')
        symbols = self._game.board_symbols
        button_state = ACTIVE if self._game.board_modifiability else DISABLED
        for x in range(3):
            for y in range(3):
                self._buttons[x][y].configure(text=symbols[x][y], state=button_state)

    def run(self):
        self._auto_move_loop()
        self._root.mainloop()

    def _auto_move_loop(self):
        is_moved = self._game.consider_auto_move()
        if is_moved:
            self._update_view()
        self._root.after(100, self._auto_move_loop)
        