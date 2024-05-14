from tkinter import *
from tkinter import messagebox
from environments.base_game_env import BaseGameEnv
from environments.game_state_enum import GameState
from players.human.human_player import HumanPlayer
from players.random.random_player import RandomPlayer

class FormApplication:
    _info_font = ('Arial', 12)
    _board_font = ('Arial', 30)
    _players_dict = {
        "Human": HumanPlayer(), 
        "Random": RandomPlayer()}

    def __init__(self):
        self._game = BaseGameEnv()
        self._player_x = HumanPlayer()
        self._player_y = RandomPlayer()
        self._root = Tk()
        self._root.title("Tic Tac Toe")
        self._create_info_section()
        self._buttons = []
        self._create_board_section()
        self._root.resizable(False, False)

    def _create_info_section(self):
        info = Frame(self._root)
        info.pack(side=TOP, fill=X, expand=True)
        status = Frame(info)
        player_x_frame = Frame(info)
        player_x_frame.grid(row=0, column=0)
        player_x_frame.grid_rowconfigure(0, minsize=50)
        player_x_frame.grid_columnconfigure(0, minsize=150)
        Label(player_x_frame, text="Player X", font=self._info_font).grid(row=0)
        player_x_str = StringVar(player_x_frame, "Human")
        self._player_x_cbox = OptionMenu(player_x_frame, player_x_str, 
                                         *self._players_dict, 
                                         command=lambda name: self._set_player(name, True))
        self._player_x_cbox.grid(row=1)
        status.grid(row=0, column=1)
        status.grid_rowconfigure(0, minsize=50)
        status.grid_columnconfigure(0, minsize=150)
        Label(status, text="Status:", font=self._info_font).grid(row=0)
        self._status_lable = Label(status, font=self._info_font)
        self._status_lable.grid(row=1)
        Button(status, text='Resetuj', font=self._info_font, command=self.restart_game).grid(row=1)
        player_y_frame = Frame(info)
        player_y_frame.grid(row=0, column=2)
        player_y_frame.grid_rowconfigure(0, minsize=50)
        player_y_frame.grid_columnconfigure(0, minsize=150)
        Label(player_y_frame, text="Player O", font=self._info_font).grid(row=0)
        player_y_str = StringVar(player_y_frame, "Random")
        self._player_y_cbox = OptionMenu(player_y_frame, player_y_str, 
                                         *self._players_dict, 
                                         command=lambda name: self._set_player(name, False))
        self._player_y_cbox.grid(row=1)

    def _create_board_section(self):
        board = Frame(self._root)
        board.pack(side=BOTTOM, fill=BOTH, expand=True)
        for x in range(3):
            row = []
            for y in range(3):
                pos = Button(board, text='', 
                             font=self._board_font, 
                             command=lambda ix=x, iy=y: self._set_position(ix, iy))
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

    def _set_player(self, name: StringVar, is_x: bool):
        new_player = self._players_dict[name]
        new_player_type = type(new_player)
        if is_x and type(self._player_x) is not new_player_type:
            self._player_x = new_player
        elif not is_x and type(self._player_y) is not new_player_type:
            self._player_y = new_player
        else: 
            return
        self.restart_game()

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