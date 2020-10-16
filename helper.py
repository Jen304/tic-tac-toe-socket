# Constant
FLAG_BUF_SIZE = 1
PACK_BUF_SIZE = 1
INT_FLAG = '!b'
END_MSG_FLAG = b'\t'
BUF_SIZE = 1024
DEFAULT_INVALID_NUM = -1

# Constant flag
YOUR_TURN = b'T'
OTHER_PLAYER_TURN = b'O'
END_GAME = b'E'
INVALID = b'I'


def recv_mes_until_end_flag(sc):
    ''' Purpose: get data from socket connection object until it gets END_MSG_FLAG
                the END_MSG_FLAG is removed from the message
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


def recv_fixed_buf_size_mes(sc, expected_size):
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
    current_size = 0
    buffer = b''
    while current_size < expected_size:
        requested_size = min(expected_size - current_size, BUF_SIZE)
        data = sc.recv(requested_size)
        buffer = buffer + data
        current_size = current_size + len(data)
    return buffer