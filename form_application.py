import tkinter as tk
from tkinter import messagebox
from environments.base_game_env import BaseGameEnv

class FormApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.restart_game()

    def restart_game(self):
        self.game = BaseGameEnv()
        self.buttons = []
        self.create_board()

    def create_board(self):
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.root, text='', font=('Arial', 30), 
                                   height=3, width=6,
                                   command=lambda idx=i*3+j: self.on_button_click(idx))
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)

    def map_game_player_symbol(self):
        if self.game.player == -1:
            return 'X'
        if self.game.player == 0:
            return ''
        if self.game.player == 1:
            return 'O'

    def on_button_click(self, idx):
        x = idx // 3
        y = idx % 3

        if self.game.is_position_taken(x, y):
            return

        player_symbol = self.map_game_player_symbol()
        self.game.move(x, y)
        self.buttons[x][y].configure(text=player_symbol)
        won_player = self.game.which_player_won()

        if self.game.is_finished == False:
            return

        if won_player == 0:
            messagebox.showinfo("Game Over", "It's a draw!")
            self.restart_game()
        else:
            messagebox.showinfo("Game Over", f"Player {player_symbol} wins!")
            self.restart_game()

root = tk.Tk()
FormApplication(root)
root.mainloop()