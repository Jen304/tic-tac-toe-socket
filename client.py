#!/usr/bin/python3

import socket
import helper
import struct

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
            * As the message will contain END_MSG_FLAG, 
            it will call recv_mes_until_end_flag() from helper
            * After receiving message, function will decode and print the message.
        Params: sc: socket connection object
    '''
    data = helper.recv_mes_until_end_flag(sc)
    msg = data.decode('utf-8')
    print(msg)

def get_input(msg):
    ''' Purpose: prompt user to enter input, get input, convert it to Integer and return it
        Return (int) input number from user
        Note: if user input is invalid (non-integer), 
            exception will be catched and function will set data to DEFAULT_INVALID_NUM
    '''
    try:
        data = int(input(msg))
    except Exception:
        data = helper.DEFAULT_INVALID_NUM
    return data

def send_input(sc, data):
    ''' Purpose: send data (number) to server. As data is integer, struck.pack uses INT_FLAG from helper
        Params: sc: socket connection object
                data: (integer) number to be sent
        Note: if struct can not pack data. Eg: in case data is very large number. 
            Exception will be catched and it will send DEFAULT_INVALID_NUM instead
    '''
    try:
        data_byte = struct.pack(helper.INT_FLAG, data)
    except Exception:
        data_byte = struct.pack(helper.INT_FLAG, helper.DEFAULT_INVALID_NUM)
    sc.sendall(data_byte)

while True:
    ''' The work flow of client
            * Get flag from server
            * Get and print board from server
            * Based on flag value, it will execute a suitable code block in if-else statement.
    '''
    try:
        flag = helper.recv_fixed_buf_size_mes(sock, helper.FLAG_BUF_SIZE)

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


    
