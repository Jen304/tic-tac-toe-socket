import struct
import board
import helper

# Note: should have check player id to avoid cheating

class GameControl:
    def __init__(self, row, col):
        self.board = board.Board(row, col)
        self.players = []
        self.current_player = None

    def add_player(self, new_player):
        self.players.append(new_player)
        welcome_mesg = "Welcome to tic tac toe game"
        new_player.send(welcome_mesg)

    def send_board(self):
        current_board = self.board.get_board_string()
        self.send_to_all_players(current_board)
    

    def check_result(self):
        '''need to add more details
        '''
        winner = self.board.check_winner()
        if winner:
            msg = '{} is winner'.format(winner)
            
            self.end_game(msg)
            return True

        tie = self.board.is_tie()
        if tie:
            msg = 'Tie'
            self.send_to_all_players(msg)
            self.end_game()
            return True

        return False

    def end_game(self, msg):
        for player in self.players:
            player.send_flag(helper.END_GAME)
            player.send(msg)
            player.exit()

    def send_to_player(self, player_id, msg):
        current_player = self.players[player_id]
        current_player.send(msg)
    
    def send_to_all_players(self, msg):
        for player in self.players:
            player.send(msg)

    def set_current_player(self, player_id):
        self.current_player = self.players[player_id]

    def play_turn(self):
        current_player = self.current_player
        current_player.send_flag(helper.YOUR_TURN)
        self.send_board()
        try:
            row = current_player.recv_integer_msg() - 1
            col = current_player.recv_integer_msg() - 1
            mark = current_player.mark
            self.board.mark(mark, row, col)
            result = self.check_result()
            if result:
                return True
            current_player.send_flag(helper.OTHER_TURN)
            
        except Exception as details:
            print(details)
            current_player.send_flag(helper.INVALID)
            return False

       
        return False
    

    