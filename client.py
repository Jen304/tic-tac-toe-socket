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

# get welcome message from server
welcome_msg = helper.recv_mes_until_end_flag(sock)
print(welcome_msg.decode('utf-8'))

# Helper function 

def get_msg(sc):
    ''' Purpose: receive and print message from server
        The message will contain end flag, 
            so recv_mes_until_end_flag() will be called in the function
        Params: sc: socket connection object
    '''
    data = helper.recv_mes_until_end_flag(sc)
    msg = data.decode('utf-8')
    print(msg)

def get_input(msg):
    ''' Purpose: prompt user to enter input, get input, convert to Integer and return it
        Return (int) number input from user
        Note: if user input is invalid (non-integer), 
        exception will be catch and function will set number to DEFAULT_INVALID_NUM
    '''
    try:
        data = int(input(msg))
    except Exception:
        data = helper.DEFAULT_INVALID_NUM
    return data

def send_input(sc, data):
    ''' Purpose: send number to server. As the data is integer, struck.pack is use with INT_FLAG
        Params: sc: socket connection object
                data: (integer) number to be sent
        Note: if struct can not pack number. Ex: number is very large. 
        Exception will be catched and it will send DEFAULT_INVALID_NUM instead
    '''
    try:
        data_byte = struct.pack(helper.INT_FLAG, data)
    except Exception:
        data_byte = struct.pack(helper.INT_FLAG, helper.DEFAULT_INVALID_NUM)
    sc.sendall(data_byte)

while True:
    ''' The work flow of client
            * Receive flag from server
            * get and print board from server
            * run the code block based on flag value
    '''
    try:
        flag = helper.recv_fixed_buf_size_mes(sock, helper.PACK_BUF_SIZE)

        get_msg(sock)
        if (flag == helper.YOUR_TURN):
            print('Your turn')
            row = get_input('Row: ')
            send_input(sock, row)
            col = get_input('Col: ')
            send_input(sock, col)

        elif(flag == helper.END_GAME):
            # get result
            get_msg(sock)
            # get out of the loop
            print('End game')
            break

        elif(flag == helper.INVALID):
            print('Invalid input\nOther player turn.')

        elif(flag == helper.OTHER_PLAYER_TURN):
            print('Other player turn')

    except Exception as details:
        print(details)


sock.close()


    
