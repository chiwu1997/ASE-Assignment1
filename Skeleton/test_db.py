import unittest
import db
from json import dumps
import sqlite3


class Test_Testdb(unittest.TestCase):
    def setUp(self):
        db.init_db()

    def tearDown(self):
        db.clear()

    def test_valid_add_move(self):
        board = [[0 for _ in range(7)] for _ in range(6)]
        board[5][0] = "red"
        board = dumps(board)
        test_tuple = ('p2', board, "", "red", "yellow", 41)
        db.add_move(test_tuple)

        conn = sqlite3.connect('sqlite_db')
        cursor = conn.execute("SELECT current_turn, board, winner, player1," +
                              "player2, remaining_moves from GAME")

        for row in cursor:
            self.assertEqual(row[0], 'p2')
            self.assertEqual(row[1], board)
            self.assertEqual(row[2], "")
            self.assertEqual(row[3], "red")
            self.assertEqual(row[4], "yellow")
            self.assertEqual(row[5], 41)

    def test_valid_get_move(self):
        board = [[0 for _ in range(7)] for _ in range(6)]
        board[5][0] = "red"
        board = dumps(board)
        test_tuple = ('p2', board, "", "red", "yellow", 41)

        conn = sqlite3.connect('sqlite_db')

        interQuery = 'INSERT INTO GAME (current_turn, board, winner,' + \
                     'player1, player2, remaining_moves)' + \
                     'VALUES ("{}", ?, "{}", "{}", "{}", {})'

        interQuery = interQuery.format(
                        test_tuple[0], test_tuple[2],
                        test_tuple[3], test_tuple[4], test_tuple[5])

        conn.execute(interQuery, (test_tuple[1],))
        conn.commit()
        conn.close()

        return_tuple = db.getMove()

        self.assertEqual(return_tuple[0], 'p2')
        self.assertEqual(return_tuple[1], board)
        self.assertEqual(return_tuple[3], "red")
        self.assertEqual(return_tuple[4], "yellow")
        self.assertEqual(return_tuple[5], 41)


# if __name__ == '__main__':
#     unittest.main()
