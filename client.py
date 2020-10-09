#!/usr/bin/python3

import socket
import helper
import struct

BUF_SIZE = 1024
HOST = '127.0.0.1'
PORT = 12345
 
# TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Initiates 3-way handshake
sock.connect((HOST, PORT)) 
# Source IP and source port
print('Client:', sock.getsockname()) 

welcome_msg = helper.recv_mes_until_end_flag(sock)
print(welcome_msg.decode('utf-8'))

def get_msg(sc):
    data = helper.recv_mes_until_end_flag(sc)
    msg = data.decode('utf-8')
    print(msg)

def get_input(msg):
    data = int(input(msg))
    return data

def send_input(sc, data):
    data_byte = struct.pack(helper.INT_FLAG, data)
    sc.sendall(data_byte)

while True:
   
    flag = helper.recv_fixed_buf_size_mes(sock, helper.PACK_BUF_SIZE)
    print(flag)
    
    if (flag == helper.YOUR_TURN):
        get_msg(sock)
        row = get_input('Row: ')
        send_input(sock, row)
        col = get_input('Col: ')
        send_input(sock, col)

    elif(flag == helper.END_GAME):
        get_msg(sock)
        break

    elif(flag == helper.INVALID):
        print('Invalid input')
        get_msg(sock)

    else:
        get_msg(sock)


sock.close()


    
