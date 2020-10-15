import helper
import struct


class Player:
    ''' Purpose: Player object holdS info about player (socket connection and mark symbol)
                help server to contact, send and receive message from player (client)
        Methods:
            send(msg):
            send_flag(msg):
            recv_integer_msg(buf_size):
            exit(): player exit the game
    '''
    def __init__(self, sock, symbol):
        self.sock = sock
        self.symbol = symbol

    def send(self, msg):
        '''Purpose: give a string, decode and tag this string with ENG_MSG_FLAG
            then send to player via socket connection

            Note: client may not read the whole message 
            if the message already contain the same character like ENG_MSG_FLAG
        '''
        msg_byte = msg.encode('utf-8') + helper.END_MSG_FLAG
        self.sock.sendall(msg_byte)

    def send_flag(self, flag):
        '''Purpose: give a flag as a byte type, send it to player via socket connection
            The purpose of this method is to make the interface for player object
            as we don't need to code like player.sock.sendall(flag) 
            and we can adjust or update the internal later if needed

            Parameter: flag (byte) a byte of character as a flag for 
            client to know what is the their next step
        '''
        self.sock.sendall(flag)

    def recv_integer_msg(self, buf_size = helper.PACK_BUF_SIZE):
        '''Purpose: receive message from client
            Because client only send number to server,
            the function uses struct.unpack to unpack the message
            Parameter: buf_size (int) expected buf_size, 
                        the default value is equal to constant PACK_BUF_SIZE
            Return:
                (int) number received from player (client)
        '''
        msg_byte = helper.recv_fixed_buf_size_mes(self.sock, buf_size)
        num = struct.unpack(helper.INT_FLAG, msg_byte)[0]
        return num

    def exit(self):
        '''Purpose: close the socket connection of player
            The purpose of this method is to create an inteface of player object
            so we don't need to write player.sock.close() and make the code more lossely tight
        '''
        self.sock.close()
        
