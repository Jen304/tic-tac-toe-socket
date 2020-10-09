# Constant
PACK_BUF_SIZE = 1
INT_FLAG = '!B'
CHAR_FLAG = '!c'
END_MSG_FLAG = b'\t'

# Constant flag
YOUR_TURN = b'T'
OTHER_TURN = b'O'
END_GAME = b'E'
INVALID = b'I'


def recv_mes_until_end_flag(sc):
    ''' Purpose: get data from socket connection object until it gets a newline ('\n')
                the newline is removed from the message
        Paramerters: 
            sc: socket connection object
        Return 
            return byte data receive from socket connection in byte type.
        Note: may cause crashes if there is not enough memory to hold byte data 
    '''
    message = b''
    buf_size = 1
    while True:
        data = sc.recv(buf_size)
        if data == END_MSG_FLAG:
            return message
        message = message + data

def recv_fixed_buf_size_mes(sc, buf_size):
    ''' Purpose: get data from socket connection object 
            until the data length is equal to buf_size
            Because sc.recv(buf_size) may receive data less than buf_size
        Parameters:
            sc: socket connection object
        Return:
            message in byte type from socket connection object 
            with the lenght is equal to buf_size
        Note: May cause crashes if the buf_size is too large 
            and machine memory can not handle it
    '''
    message = b''
    while True:
        data = sc.recv(buf_size - len(message))
        message = message + data
        if len(message) == buf_size:
            return message