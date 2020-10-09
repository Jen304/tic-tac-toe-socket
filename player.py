import helper
import struct


class Player:
    def __init__(self, sock, mark):
        self.sock = sock
        self.mark = mark

    def send(self, msg):
        msg_byte = msg.encode('utf-8') + helper.END_MSG_FLAG
        self.sock.sendall(msg_byte)

    def send_flag(self, flag):
        self.sock.sendall(flag)


    def recv_integer_msg(self, buf_size = helper.PACK_BUF_SIZE):
        msg_byte = helper.recv_fixed_buf_size_mes(self.sock, buf_size)
        num = struct.unpack(helper.INT_FLAG, msg_byte)[0]
        return num

    def exit(self):
        self.sock.close()
        
