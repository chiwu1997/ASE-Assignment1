from flask import Flask, render_template, request, redirect, jsonify
from json import dump
from Gameboard import Gameboard
import db


app = Flask(__name__)

import logging
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
    game = Gameboard()   # initialization for a new game
    return render_template('player1_connect.html', status = "Pick a Color.")


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
    color = request.args.get('color')   # get color from HTTP argument
    game.player1 = color                # set up player1's color
    return render_template('player1_connect.html', status = "Color picked")


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
    if game.player1 == "":   # if p1 didn't pick a color -> Error
        return 'Player1 should pick a color first!'
    game.player2 = "yellow" if game.player1 == "red" else "red"   # set up player2's color
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
    if game.game_result != "":
        return jsonify(move= game.board, invalid = True)
    col = int(request.json["column"][-1]) - 1
    invalid, winner, reason = game.move(col, 'p1')
    if invalid:
        return jsonify(move= game.board, invalid = True, reason = reason, winner = winner)
    return jsonify (move= game.board, invalid=False, winner = winner)

'''
Same as '/move1' but instead proccess Player 2
'''


@app.route('/move2', methods=['POST'])
def p2_move():
    global game
    if game.game_result != "":
        return jsonify(move= game.board, invalid = True)
    col = int(request.json["column"][-1]) - 1
    invalid, winner, reason = game.move(col, 'p2')
    if invalid:
        return jsonify(move= game.board, invalid = True, reason = reason, winner = winner)
    return jsonify (move= game.board, invalid=False, winner = winner)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
