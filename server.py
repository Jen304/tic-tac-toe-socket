#!/usr/bin/python3

import threading, socket
from game_control import GameControl
from player import Player
import helper


locks = []
players = []

# constant for socket
HOST = ''
PORT = 12345
NUM_CONNECTIONS = 2

# constant for the game
NUM_ROWS = 5
NUM_COLS = 5
PLAYER_SYMBOLS = ['X', 'O']

for i in range(2):
    locks.append(threading.Semaphore())
    locks[-1].acquire()

## create a player list to have to player and will send the message to each
# send the board for both
# send the turn for elibible player (send message to ask)
# check the board
# if having winner => send message to 2 players and terminate connection, break the loop

def contactPlayer(player_id):

    while True:
        locks[player_id].acquire()
        global game_control
        game_control.set_current_player(player_id)
        has_result = game_control.play_turn()
        if(has_result):
            break
        
        next_player = (player_id + 1) % 2
        locks[next_player].release()

# TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# claim messages send to port "PORT"
sock.bind((HOST, PORT))

sock.listen(NUM_CONNECTIONS)
# print source IP and port
print('Server: ', sock.getsockname())

# init game control object
game_control = GameControl(NUM_ROWS, NUM_COLS)


# only accept 2 connection
for player_id in range(NUM_CONNECTIONS):
    # wait until a connection is established
    sc, sockname = sock.accept()
    new_player = Player(sc, PLAYER_SYMBOLS[player_id])
    game_control.add_player(new_player)
    print('Client connected:', sc.getpeername()) 
    threading.Thread(target = contactPlayer, args = (player_id, )).start()
game_control.players[1].send_flag(helper.OTHER_TURN)
locks[0].release()
