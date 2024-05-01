class BaseGameEnv:
    def __init__(self):
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.player = -1
        self.win_player = 0
    
    def which_player_move(self):
        return self.player
    
    def which_player_won(self):
        return self.win_player
    
    def check_win(self):
        if self.win_player != 0:
            pass

        c1 = self.board[0][0] + self.board[0][1] + self.board[0][2]
        if abs(c1) == 3:
            self.win_player = self.player

        c2 = self.board[1][0] + self.board[1][1] + self.board[1][2]
        if abs(c2) == 3:
            self.win_player = self.player
        
        c3 = self.board[2][0] + self.board[2][1] + self.board[2][2]
        if abs(c3) == 3:
            self.win_player = self.player
        
        r1 = self.board[0][0] + self.board[1][0] + self.board[2][0]
        if abs(r1) == 3:
            self.win_player = self.player

        r2 = self.board[0][1] + self.board[1][1] + self.board[2][1]
        if abs(r2) == 3:
            self.win_player = self.player

        r3 = self.board[0][2] + self.board[1][2] + self.board[2][2]
        if abs(r3) == 3:
            self.win_player = self.player

        b1 = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if abs(b1) == 3:
            self.win_player = self.player

        b2 = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if abs(b2) == 3:
            self.win_player = self.player
    
    def move(self, x: int, y: int):
        if self.win_player != 0:
            raise Exception(f'The game is finished.')
        
        if self.board[x][y] != 0:
            raise Exception(f'Position ({x},{y}) is already taken.')
        
        self.board[x][y] = self.player

        self.check_win()

        self.player *= -1