import sqlite3
from sqlite3 import Error

'''
Initializes the Table GAME
Do not modify
'''


def init_db():
    # creates Table
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute('CREATE TABLE GAME(current_turn TEXT, board TEXT,' +
                     'winner TEXT, player1 TEXT, player2 TEXT' +
                     ', remaining_moves INT)')
        print('Database Online, table created')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


'''
move is a tuple (current_turn, board, winner, player1, player2,
remaining_moves)
Insert Tuple into table
'''


def add_move(move):  # will take in a tuple
    conn = sqlite3.connect('sqlite_db')
    cursor = conn.execute("SELECT current_turn from GAME")

    if len(list(cursor)) >= 1:
        conn.execute('DELETE FROM GAME;')

    interQuery = 'INSERT INTO GAME (current_turn, board, winner,' + \
                 'player1, player2, remaining_moves)' + \
                 'VALUES ("{}", ?, "{}", "{}", "{}", {})'

    interQuery = interQuery.format(
                    move[0], move[2],
                    move[3], move[4], move[5])

    conn.execute(interQuery, (move[1],))

    conn.commit()
    conn.close()


'''
Get the last move played
return (current_turn, board, winner, player1, player2, remaining_moves)
'''


def getMove():
    # will return tuple(current_turn, board, winner, player1, player2,
    # remaining_moves) or None if db fails
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        cursor = conn.execute("SELECT current_turn, board, winner, player1," +
                              "player2, remaining_moves from GAME")

        for row in cursor:
            return row

    except Error:
        return None

    finally:
        if conn:
            conn.close()


'''
Clears the Table GAME
Do not modify
'''


def clear():
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute("DROP TABLE GAME")
        print('Database Cleared')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


# init_db()
# move = ('p1', str(((0 for x in range(7)) for y in range(6))),
#         "", "red", "yellow", 42)
# add_move(move)
# print(getMove())

# move = ('p2', str(((0 for x in range(7)) for y in range(6))),
#         "", "red", "yellow", 41)
# add_move(move)
# print(getMove())

# clear()
