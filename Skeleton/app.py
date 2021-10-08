from flask import Flask, render_template, request, jsonify
# from flask import redirect
from json import loads
from Gameboard import Gameboard
import db
import logging


app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

game = None

'''
Implement '/' endpoint
Method Type: GET
return: template player1_connect.html and status = "Pick a Color."
Initial Webpage where gameboard is initialized
'''


@app.route('/', methods=['GET'])
def player1_connect():
    global game
    db.clear()
    db.init_db()
    game = Gameboard()   # initialization for a new game
    return render_template('player1_connect.html', status="Pick a Color.")


'''
Helper function that sends to all boards don't modify
'''


@app.route('/autoUpdate', methods=['GET'])
def updateAllBoards():
    try:
        return jsonify(move=game.board, winner=game.game_result,
                       color=game.player1)
    except Exception:
        return jsonify(move="")


'''
Implement '/p1Color' endpoint
Method Type: GET
return: template player1_connect.html and status = <Color picked>
Assign player1 their color
'''


@app.route('/p1Color', methods=['GET'])
def player1_config():
    global game
    if game and game.player2:
        return render_template('player1_connect.html', status="Color picked")

    if not game:
        game = Gameboard()
        current_state = db.getMove()
        print(current_state[3])
        if current_state:
            game.current_turn = current_state[0]
            game.board = loads(current_state[1])
            game.winner = current_state[2]
            game.player1 = current_state[3]
            game.player2 = current_state[4]
            game.remaining_moves = current_state[5]

    else:
        color = request.args.get('color')   # get color from HTTP argument
        game.player1 = color                # set up player1's color

    return render_template('player1_connect.html', status="Color picked")


'''
Implement '/p2Join' endpoint
Method Type: GET
return: template p2Join.html and status = <Color picked> or Error
if P1 didn't pick color first

Assign player2 their color
'''


@app.route('/p2Join', methods=['GET'])
def p2Join():
    global game
    if not game:
        game = Gameboard()
        current_state = db.getMove()
        if current_state:
            game.current_turn = current_state[0]
            game.board = loads(current_state[1])
            game.winner = current_state[2]
            game.player1 = current_state[3]
            game.player2 = current_state[4]
            game.remaining_moves = current_state[5]

    else:
        # if p1 didn't pick a color -> Error
        if game.player1 == "":
            return 'Player1 should pick a color first!'

        # set up player2's color
        game.player2 = "yellow" if game.player1 == "red" else "red"

    return render_template('p2Join.html')


'''
Implement '/move1' endpoint
Method Type: POST
return: jsonify (move=<CurrentBoard>,
invalid=True or False, winner = <currWinner>)
If move is valid --> invalid = False else invalid = True
If invalid == True, also return reason= <Why Move is Invalid>

Process Player 1's move
'''


@app.route('/move1', methods=['POST'])
def p1_move():
    global game
    if game.is_game_over():
        return jsonify(move=game.board, invalid=True)
    col = int(request.json["column"][-1]) - 1
    invalid, winner, reason = game.move(col, 'p1')
    if invalid:
        return jsonify(
            move=game.board,
            invalid=True, reason=reason,
            winner=winner
        )
    return jsonify(move=game.board, invalid=False, winner=winner)


'''
Same as '/move1' but instead proccess Player 2
'''


@app.route('/move2', methods=['POST'])
def p2_move():
    global game
    if game.is_game_over():
        return jsonify(move=game.board, invalid=True)
    col = int(request.json["column"][-1]) - 1
    invalid, winner, reason = game.move(col, 'p2')
    if invalid:
        return jsonify(
            move=game.board,
            invalid=True,
            reason=reason,
            winner=winner
        )
    return jsonify(move=game.board, invalid=False, winner=winner)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
