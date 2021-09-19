import db

class Gameboard():
    def __init__(self):
        self.player1 = ""
        self.player2 = ""
        self.board = [[0 for x in range(7)] for y in range(6)]
        self.game_result = ""
        self.current_turn = 'p1'
        self.remaining_moves = 42

    def is_current_turn(self, player):
        return player == self.current_turn

    def is_column_full(self, col):
        return self.board[0][col] != 0

    def move(self, col, player):
        if self.remaining_moves == 0:   # all spaces are used up
            return False, "Draw", None

        if not self.is_current_turn(player):   # player need to take turns to move
            return True, "", "Not your turn".format(player)
        
        if self.is_column_full(col):   # check whether the column is full
            return True, "", "The column is full"
        
        # Move operation
        row = None
        color = self.player1 if player == 'p1' else self.player2
        for i in range(5, -1, -1):
            if self.board[i][col] == 0:
                self.board[i][col] = color
                row = i
                break
        
        # check if current play wins or not
        if self.check_winner(row, col, color):
            self.game_result = player
            return False, player, None
        
        # update the status and continue the game
        self.current_turn = "p2" if self.current_turn == "p1" else "p1"
        self.remaining_moves -= 1
        return False, "", None

    def check_winner(self, x, y, color):
        CONNECT = 3

        def is_valid(v, min, max):
            return min <= v <= max

        def connect(x, y, color, dx, dy):
            count = 0
            for i in range(CONNECT):
                tx = x + dx[i]
                ty = y + dy[i]
                if not is_valid(tx, 0, 5) or not is_valid(ty, 0, 6):
                    continue
                if self.board[tx][ty] == color:
                    count += 1
                else:
                    break
            return count

        assess = [0 for _ in range(4)]   # 四個方向
        fixed = [0 for _ in range(CONNECT)]
        forward = [i+1 for i in range(CONNECT)]
        reverse = [-(i+1) for i in range(CONNECT)]
        assess[0] = connect(x, y, color, forward, fixed) + connect(x, y, color, reverse, fixed) + 1
        assess[1] = connect(x, y, color, fixed, forward) + connect(x, y, color, fixed, reverse) + 1
        assess[2] = connect(x, y, color, reverse, reverse) + connect(x, y, color, forward, forward) + 1
        assess[3] = connect(x, y, color, reverse, forward) + connect(x, y, color, forward, reverse) + 1
        return max(assess) >= 4

'''
Add Helper functions as needed to handle moves and update board and turns
'''


    
