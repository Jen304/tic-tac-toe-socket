#!/usr/bin/python3

import threading, socket
from game_control import GameControl
from player import Player
import helper

# constant for socket
HOST = ''
PORT = 12345

# constant for the game
NUM_ROWS = 5
NUM_COLS = 5
NUM_PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O']

# Create single-marble semaphore for each player
locks = []
for i in range(NUM_PLAYERS):
    locks.append(threading.Semaphore())
    locks[-1].acquire()


def contactPlayer(player_id, game_control):
    while True:
        locks[player_id].acquire()
        game_control.set_current_player(player_id)
        has_result = game_control.play_turn()
        if(has_result):
            break    
        next_player = (player_id + 1) % 2
        locks[next_player].release()

# TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    # claim messages send to port "PORT"
    sock.bind((HOST, PORT))
except Exception as e:
    print(e)
    sys.exit(-1)
# listent to NUMPLAYERS connections
sock.listen(NUM_PLAYERS)
# print source IP and port
print('Server: ', sock.getsockname())

# init game control object
game_control = GameControl(NUM_ROWS, NUM_COLS)
new_player = None
# only accept NUM_PLAYERS connections
for player_id in range(NUM_PLAYERS):
    # wait until a connection is established
    sc, sockname = sock.accept()
    # create new_player
    new_player = Player(sc, PLAYER_SYMBOLS[player_id])
    # add new_player to game_control
    game_control.add_player(new_player)
    print('Client connected:', sc.getpeername()) 
    threading.Thread(target = contactPlayer, args = (player_id, game_control)).start()

# send second player flag that the first turn is other player
new_player.send_flag(helper.OTHER_PLAYER_TURN)
locks[0].release()

