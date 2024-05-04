class BaseGameEnv:
    def __init__(self):
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.player = -1
        self.is_finished = False
        self.win_player = 0
        self.moves_count = 0
    
    def which_player_move(self):
        return self.player
    
    def which_player_won(self):
        return self.win_player
    
    def check_state(self):
        if self.is_finished == True:
            return

        c1 = self.board[0][0] + self.board[0][1] + self.board[0][2]
        if abs(c1) == 3:
            self.win_player = self.player
            self.is_finished = True

        c2 = self.board[1][0] + self.board[1][1] + self.board[1][2]
        if abs(c2) == 3:
            self.win_player = self.player
            self.is_finished = True
        
        c3 = self.board[2][0] + self.board[2][1] + self.board[2][2]
        if abs(c3) == 3:
            self.win_player = self.player
            self.is_finished = True
        
        r1 = self.board[0][0] + self.board[1][0] + self.board[2][0]
        if abs(r1) == 3:
            self.win_player = self.player
            self.is_finished = True

        r2 = self.board[0][1] + self.board[1][1] + self.board[2][1]
        if abs(r2) == 3:
            self.win_player = self.player
            self.is_finished = True

        r3 = self.board[0][2] + self.board[1][2] + self.board[2][2]
        if abs(r3) == 3:
            self.win_player = self.player
            self.is_finished = True

        b1 = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if abs(b1) == 3:
            self.win_player = self.player
            self.is_finished = True

        b2 = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if abs(b2) == 3:
            self.win_player = self.player
            self.is_finished = True

        if self.moves_count > 8:
            self.is_finished = True
    
    def move(self, x: int, y: int):
        if self.win_player != 0:
            raise Exception(f'The game is finished.')
        
        if self.board[x][y] != 0:
            raise Exception(f'Position ({x},{y}) is already taken.')
        
        self.board[x][y] = self.player

        self.moves_count += 1

        self.check_state()

        self.player *= -1
    
    def is_position_taken(self, x: int, y: int):
        return self.board[x][y] != 0