import struct
import board
import helper

class GameControl:
    '''Purpose: Control the game flow
        Methods:
            add_player(new_player): add a player to the game
            check_result(): check the result (has winner or tie). If it has the result, it will call end_game method
            end_game(): send flag and msg to 2 players to notify result and end the game
            send_to_all_players(msg): send message to all players in players list
            play_turn(player_id): run the flow of each turn

    '''
    def __init__(self, board_size):
        self.board = board.Board(board_size)
        self.players = []

    def add_player(self, new_player):
        '''Purpose: append the player object to players list
                send welcome message to player and notify what is their symbol for this game
        '''
        self.players.append(new_player)
        welcome_mesg = "Welcome to tic tac toe game. You are {}".format(new_player.symbol)
        size = len(welcome_mesg)
        new_player.send_packed_msg(helper.WELCOME)
        new_player.send_packed_msg(size)
        new_player.send(welcome_mesg)    

    def check_result(self):  
        ''' Purpose: check current board whether is has winner, tie or no result
            if board.check_winner() or board.is_tie() return non-false value,
            it will call end_game method and send result message to end the game.
        '''    
        winner = self.board.check_winner()
        if winner:
            msg = '{} is winner'.format(winner)
            self.end_game(msg)
            return True

        tie = self.board.is_tie()
        if tie:
            msg = 'Tie'
            self.end_game(msg)
            return True
        return False

    def end_game(self, msg):
        '''Purpose": notify 2 players know that the game is ended.
            It will send END_GAME flag, lastest board state and result message to all players
            After that it will close connection to each player
        '''
        for player in self.players:
            player.send_packed_msg(helper.END_GAME)
            current_board = self.board.get_board_string()
            player.send_packed_msg(len(msg))
            player.send(msg)
            
    
    def send_to_all_players(self, msg):
        '''Purpose: give a message in string type and send to each player in players list
            through send() method of Player object
        '''
        for player in self.players:
            player.send(msg)

    def play_turn(self, player_id):
        '''Purpose: run the game flow for each turn
            The game flow is: 
                * Update current_player based on player_id
                * Send YOUR_TURN flag to current_player
                * Send board state (string) to all players
                * Reiceive row and column values from current_player
                * Mark current_player symbol on the board. 
                    If row and column values are invalid, Exception will be catched
                * Check result. Call check_result() method.
                * Return True if game has result, otherwise, False value will be returned
            Params: (int) player_id: id of player in the current turn.
            Return:
                (boolean) True if the game has result (has winner or tie) 
                    or False if it does not yet.
            Exceptions: exception can be raised when marking the board. 
                In this case, INVALID flag will be sent to current player 
                and current player will loose the curent turn.
        '''
        current_player = self.players[player_id]
        current_player.send_packed_msg(helper.YOUR_TURN)
        current_board = self.board.get_board_string()
        current_player.send_packed_msg(len(current_board))
        current_player.send(current_board)
        try:
            row = current_player.recv_integer_msg() 
            col = current_player.recv_integer_msg() 
            
            self.board.mark(current_player.symbol, row, col)
            result = self.check_result()
            if result:
                return True   
        except Exception as details:
            print(details)
            return False
        return False
    