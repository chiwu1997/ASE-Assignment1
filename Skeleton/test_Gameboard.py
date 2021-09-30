import unittest
from Gameboard import Gameboard


class Test_TestGameboard(unittest.TestCase):
    def setUp(self):
        self.game = Gameboard()
        self.game.player1 = "red"
        self.game.player2 = "yellow"

    def test_valid_move(self):
        # 1. Check happy path for correct move
        self.game.move(0, 'p1')
        self.assertEqual(self.game.board[5][0], self.game.player1)
        self.game.move(1, 'p2')
        self.assertEqual(self.game.board[5][1], self.game.player2)

    def test_invalid_move(self):
        # 1. Check happy path for correct move
        # Invalid move: player1 moves before picking a color
        self.game.player1 = ""
        self.game.player2 = ""
        self.assertEqual(
            self.game.move(3, 'p1'),
            (True, "", "Player1 should pick a color first!")
            )

    def test_is_current_turn(self):
        # 2. Check if is the current player's turn
        self.assertEqual(self.game.move(0, 'p2'), (True, "", "Not your turn"))
        self.game.move(0, 'p1')
        self.assertEqual(self.game.move(1, 'p1'), (True, "", "Not your turn"))

    def test_is_game_over(self):
        # 3. Check if winner was already declared
        game = Gameboard()
        game.game_result = 'p1'
        self.assertEqual(game.is_game_over(), True)
        game.game_result = ''
        self.assertEqual(game.is_game_over(), False)

    def test_is_draw(self):
        # 4. Check if the game is tied
        # Case1: The game is over and tied
        self.game.board = [
            ["yellow", "yellow", "yellow", "red", "red", "red", "yellow"],
            ["red", "red", "red", "yellow", "yellow", "yellow", "red"],
            ["yellow", "yellow", "yellow", "red", "red", "red", "yellow"],
            ["red", "red", "red", "yellow", "yellow", "yellow", "red"],
            ["yellow", "yellow", "yellow", "red", "red", "red", "yellow"],
            ["red", "red", "red", "yellow", "yellow", "yellow", "red"]
        ]
        self.game.remaining_moves = 0
        self.assertEqual(self.game.move(0, 'p1'), (False, "Draw", None))

        # Case2: Last move and the game is tied in the end
        self.game.board = [
            ["yellow", "yellow", "yellow", "red", "red", "yellow", 0],
            ["red", "red", "red", "yellow", "red", "red", "yellow"],
            ["yellow", "yellow", "yellow", "red", "red", "red", "yellow"],
            ["red", "red", "red", "yellow", "yellow", "red", "yellow"],
            ["yellow", "yellow", "yellow", "red", "red", "yellow", "red"],
            ["red", "red", "red", "yellow", "red", "yellow", "yellow"]
        ]
        self.game.current_turn = 'p2'
        self.game.remaining_moves = 1
        self.assertEqual(self.game.move(6, 'p2'), (False, "p2", None))

        # Case3: Last move and player2 wins the game
        self.game.board = [
            ["yellow", "yellow", "yellow", "red", "red", "red", 0],
            ["red", "red", "red", "yellow", "yellow", "yellow", "red"],
            ["yellow", "yellow", "yellow", "red", "red", "red", "yellow"],
            ["red", "red", "red", "yellow", "yellow", "yellow", "red"],
            ["yellow", "yellow", "yellow", "red", "red", "red", "yellow"],
            ["red", "red", "red", "yellow", "yellow", "yellow", "red"]
        ]
        self.game.current_turn = 'p2'
        self.game.remaining_moves = 1
        self.assertEqual(self.game.move(6, 'p2'), (False, "Draw", None))

    def test_is_column_full(self):
        # 5. Check if the current column is filled
        for i in range(5, 0, -2):
            self.game.board[i][0] = self.game.player1
        for i in range(4, -1, -2):
            self.game.board[i][0] = self.game.player2
        self.game.remaining_moves = 36
        self.assertEqual(
            self.game.move(0, 'p1'),
            (True, "", "The column is full")
        )

    def test_winning_move_horizontal(self):
        # Checks if there is a winning move in horizontal direction
        for i in range(3):
            self.game.board[5][i] = self.game.player1
            self.game.board[4][i] = self.game.player2
        self.game.remaining_moves = 36
        self.game.move(3, 'p1')
        self.assertEqual(self.game.game_result, 'p1')

    def test_winning_move_vertical(self):
        # Checks if there is a winning move in vertical direction
        for i in range(3):
            self.game.board[5-i][0] = self.game.player1
            self.game.board[5-i][1] = self.game.player2
        self.game.remaining_moves = 36
        self.game.move(0, 'p1')
        self.assertEqual(self.game.game_result, 'p1')

    def test_winning_move_positive_slope_diagonal(self):
        # Checks if there is a winning move in positive diagonal direction
        self.game.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, "red", "yellow", 0, 0, 0],
            [0, "red", "yellow", "red", "yellow", 0, 0],
            ["red", "yellow", "yellow", "red", 0, 0, 0]
        ]
        self.game.remaining_moves = 32
        self.game.move(3, 'p1')
        self.assertEqual(self.game.game_result, 'p1')

    def test_winning_move_negative_slope_diagonal(self):
        # Checks if there is a winning move in negative diagonal direction
        self.game.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            ["red", "red", 0, 0, 0, 0, 0],
            ["yellow", "red", 0, 0, 0, 0, 0],
            ["red", "yellow", "red", 0, 0, 0, 0],
            ["yellow", "yellow", "yellow", 0, 0, 0, 0]
        ]
        self.game.remaining_moves = 32
        self.game.move(3, 'p1')
        self.assertEqual(self.game.game_result, 'p1')


# if __name__ == '__main__':
#     unittest.main()
