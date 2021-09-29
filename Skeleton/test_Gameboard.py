import unittest
from Gameboard import Gameboard


class Test_TestGameboard(unittest.TestCase):
    def test_move(self):
        # 1. Check happy path for correct move
        game = Gameboard()
        game.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, "red", 0, 0, 0, 0],
            ["yellow", "yellow", "yellow", 0, 0, 0, 0],
            ["red", "red", "red", 0, 0, 0, 0]
        ]
        game.current_turn = 'p2'
        game.player1 = "red"
        game.player2 = "yellow"
        game.remaining_moves = 35

        # Valid move part 1
        ANSWER1 = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, "red", 0, 0, 0, 0],
            ["yellow", "yellow", "yellow", 0, 0, 0, 0],
            ["red", "red", "red", "yellow", 0, 0, 0]
        ]
        game.move(3, 'p2')
        self.assertEqual(game.board, ANSWER1)

        # Valid move part 2
        ANSWER2 = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, "red", 0, 0, 0, 0],
            ["yellow", "yellow", "yellow", "red", 0, 0, 0],
            ["red", "red", "red", "yellow", 0, 0, 0]
        ]
        game.move(3, 'p1')
        self.assertEqual(game.board, ANSWER2)

        # Invalid move: player1 moves before picking a color
        ANSWER2 = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ]
        game.current_turn = 'p1'
        game.player1 = ""
        game.player2 = ""
        game.remaining_moves = 42
        self.assertEqual(
            game.move(3, 'p1'),
            (True, "", "Player1 should pick a color first!")
            )

    def test_is_current_turn(self):
        # 2. Check if is the current player's turn
        game = Gameboard()
        game.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, "red", 0, 0, 0, 0],
            ["yellow", "yellow", "yellow", 0, 0, 0, 0],
            ["red", "red", "red", 0, 0, 0, 0]
        ]
        game.current_turn = 'p2'
        game.player1 = "red"
        game.player2 = "yellow"
        game.remaining_moves = 35
        self.assertEqual(game.move(0, 'p1'), (True, "", "Not your turn"))
        self.assertEqual(game.move(1, 'p1'), (True, "", "Not your turn"))

    def test_is_game_over(self):
        # 3. Check if winner was already declared
        game = Gameboard()
        game.game_result = 'p1'
        self.assertEqual(game.is_game_over(), True)
        game.game_result = ''
        self.assertEqual(game.is_game_over(), False)

    def test_is_draw(self):
        # 4. Check if the game is tied
        game = Gameboard()
        # Case1: The game is over and tied
        game.board = [
            ["yellow", "yellow", "yellow", "red", "red", "red", "yellow"],
            ["red", "red", "red", "yellow", "yellow", "yellow", "red"],
            ["yellow", "yellow", "yellow", "red", "red", "red", "yellow"],
            ["red", "red", "red", "yellow", "yellow", "yellow", "red"],
            ["yellow", "yellow", "yellow", "red", "red", "red", "yellow"],
            ["red", "red", "red", "yellow", "yellow", "yellow", "red"]
        ]
        game.current_turn = 'p1'
        game.player1 = "red"
        game.player2 = "yellow"
        game.remaining_moves = 0
        self.assertEqual(game.move(0, 'p1'), (False, "Draw", None))
        # Case2: Last move and the game is tied in the end
        game.board = [
            ["yellow", "yellow", "yellow", "red", "red", "yellow", 0],
            ["red", "red", "red", "yellow", "red", "red", "yellow"],
            ["yellow", "yellow", "yellow", "red", "red", "red", "yellow"],
            ["red", "red", "red", "yellow", "yellow", "red", "yellow"],
            ["yellow", "yellow", "yellow", "red", "red", "yellow", "red"],
            ["red", "red", "red", "yellow", "red", "yellow", "yellow"]
        ]
        game.current_turn = 'p2'
        game.player1 = "red"
        game.player2 = "yellow"
        game.remaining_moves = 1
        self.assertEqual(game.move(6, 'p2'), (False, "p2", None))
        # Case3: Last move and player2 wins the game
        game.board = [
            ["yellow", "yellow", "yellow", "red", "red", "red", 0],
            ["red", "red", "red", "yellow", "yellow", "yellow", "red"],
            ["yellow", "yellow", "yellow", "red", "red", "red", "yellow"],
            ["red", "red", "red", "yellow", "yellow", "yellow", "red"],
            ["yellow", "yellow", "yellow", "red", "red", "red", "yellow"],
            ["red", "red", "red", "yellow", "yellow", "yellow", "red"]
        ]
        game.current_turn = 'p2'
        game.player1 = "red"
        game.player2 = "yellow"
        game.remaining_moves = 1
        self.assertEqual(game.move(6, 'p2'), (False, "Draw", None))

    def test_is_column_full(self):
        # 5. Check if the current column is filled
        game = Gameboard()
        game.board = [
            ["yellow", 0, 0, 0, 0, 0, 0],
            ["red", 0, 0, 0, 0, 0, 0],
            ["yellow", 0, 0, 0, 0, 0, 0],
            ["red", 0, 0, 0, 0, 0, 0],
            ["yellow", 0, 0, 0, 0, 0, 0],
            ["red", 0, 0, 0, 0, 0, 0]
        ]
        game.current_turn = 'p1'
        game.player1 = "red"
        game.player2 = "yellow"
        game.remaining_moves = 36
        self.assertEqual(game.move(0, 'p1'), (True, "", "The column is full"))

    def test_check_winner(self):
        # 6. Check happy path for winning move in each of
        # horizontal, vertical, positive/negative slope diagonal
        game = Gameboard()
        # Horizontal
        game.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            ["yellow", "yellow", "yellow", 0, 0, 0, 0],
            ["red", "red", "red", 0, 0, 0, 0]
        ]
        game.current_turn = 'p1'
        game.player1 = "red"
        game.player2 = "yellow"
        game.remaining_moves = 36
        game.move(3, 'p1')
        self.assertEqual(game.game_result, 'p1')
        # Vertical
        game.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            ["red", "yellow", 0, 0, 0, 0, 0],
            ["red", "yellow", 0, 0, 0, 0, 0],
            ["red", "yellow", 0, 0, 0, 0, 0]
        ]
        game.current_turn = 'p1'
        game.player1 = "red"
        game.player2 = "yellow"
        game.remaining_moves = 36
        game.move(0, 'p1')
        self.assertEqual(game.game_result, 'p1')
        # positive slope diagonal
        game.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, "red", "yellow", 0, 0, 0],
            [0, "red", "yellow", "red", "yellow", 0, 0],
            ["red", "yellow", "yellow", "red", 0, 0, 0]
        ]
        game.current_turn = 'p1'
        game.player1 = "red"
        game.player2 = "yellow"
        game.remaining_moves = 32
        game.move(3, 'p1')
        self.assertEqual(game.game_result, 'p1')
        # negative slope diagonal
        game.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            ["red", 0, 0, 0, 0, 0, 0],
            ["yellow", "red", 0, 0, 0, 0, 0],
            ["red", "yellow", "red", 0, 0, 0, 0],
            ["yellow", "yellow", "yellow", 0, 0, 0, 0]
        ]
        game.current_turn = 'p2'
        game.player1 = "yellow"
        game.player2 = "red"
        game.remaining_moves = 33
        game.move(3, 'p2')
        self.assertEqual(game.game_result, 'p2')


# if __name__ == '__main__':
#     unittest.main()
