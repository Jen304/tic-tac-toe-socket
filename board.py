DEFAULT_MARK= '_'

class Board: 
    ''' Purpose: Board object holds information about board state, num rows and num cols
        Methods:
            mark(mark, row, rol): mark player's symbol on a position of the board based on row and col
            get_board_string(): get current board in string type that can be presented on the terminal for players
            check_winner(): check if the current board has a winner or not
            check_cols(): check winner on each column
            check_rows(): check winner on each row
            check_diagonal_left_to_right(): check winner on left-to-right diagonal direction 
            check_diagonal_right_to_left(): check winner on right-to-left diagonal direction
    '''
    def __init__(self, num_rows, num_cols):
        self.board = []
        self.rows = num_rows
        self.cols = num_cols
        self.board = [ [DEFAULT_MARK] * num_cols for i in range(num_rows)]

        
    def mark(self, mark, row, col):
        ''' Purpose: mark a symbol on the board based on row and col
            Params: mark(string): symbol to mark
                    row(int) row number from player input
                    col(int) col number from player input
            Note: if row and col are less than 1, out of array length 
                or that position already marked, it will raise an exception
        '''
        # check if row and col is valid to set in array
        if(row < 1 or col < 1):
            raise Exception('Invalid')
        index_row = row - 1
        index_col = col - 1
        # check if the posion is already marked
        if(self.board[index_row][index_col] != DEFAULT_MARK):
            raise Exception('Invalid')
        self.board[index_row][index_col] = mark

    def get_board_string(self):
        ''' Purpose:  get current board in string type that can be presented on terminal for players.
                a new line will be inserted at the end of each line, for presentation purpose
                each element in a row will be separated by a space
            Return: (string) current board state
        '''
        board_str = ''
        for row in self.board:
            board_str = board_str + ''.join([str(elem) + ' ' for elem in row]) + '\n'
        print(board_str)
        return board_str

    def check_winner(self):
        ''' Purpose: check the winner in the board
                    the method will call check_col, check_row, check_diagonal_left_to_right 
                    and check_diagonal_right_to_left repspectively unitl it gets winner symbol 
                    or None value will be returned
            Return: (string) winner symbol or None
        '''
        winner = None
        winner = self.check_col()
        if(not winner):
            winner = self.check_row()
        if(not winner):
            winner = self.check_diagonal_left_to_right()
        if(not winner):
            winner = self.check_diagonal_right_to_left()
        return winner

    def check_col(self):
        ''' Purpose: iterate each column to check winner
                if all elements in a column are not DEFAULT_MARK and identical, 
                winner will be determined, and winner symbol (string) will be returned
            Returns: (string) winner symbol or None
        '''
        col = 0
        winner = None
        while col < self.cols:
            item = self.board[0][col]
            if(item != DEFAULT_MARK):
                all_matched = True
                for row in range(self.rows):
                    if item != self.board[row][col]:
                        all_matched = False
                        break
                if(all_matched):
                    winner = self.board[0][col]
                    break
            col = col + 1
            
        return winner

    def check_row(self):
        ''' Purpose: iterate each row to check winner
                if all elements in a row are not DEFAULT_MARK and identical, 
                winner will be determined, and winner symbol (string) will be returned
            Returns:  (string) winner symbol or None
        '''
        winner = None
        for row in self.board:
            checking_item = row[0]
            if (checking_item != DEFAULT_MARK):
                if all(checking_item == item for item in row):
                    winner = row[0]
                    break
        return winner

    def check_diagonal_left_to_right(self):
        ''' Purpose: check winner on left-to-right diagonal direction
                if all elements in left-to-right diagonal direction are not DEFAULT_MARK and identical, 
                winner will be determined, and winner symbol (string) will be returned
            Returns:  (string) winner symbol or None
        '''
        item = self.board[0][0]
        if(item == DEFAULT_MARK):
            return None
        i = 1
        while i < self.rows:
            if item != self.board[i][i]:
                return None
            i = i + 1
        return item

    def check_diagonal_right_to_left(self):
        ''' Purpose: check winner on right-to-left diagonal direction
                if all elements in right-to-left diagonal direction are not DEFAULT_MARK and identical, 
                winner will be determined, and winner symbol (string) will be returned
            Returns:  (string) winner symbol or None
        '''
        item = self.board[0][-1]
        if(item == DEFAULT_MARK):
            return None
        i = 1
        while i < self.rows:
            if item != self.board[i][self.cols - 1 - i]:
                return None
            i = i + 1
        return item

    def is_tie(self):
        ''' Purpose: check if the board is tie (fullly marked or no DEFAULT_MARK left) 
            Return (boolean) True if the board is tie or False if not
        '''
        is_full = True
        for row in self.board:
            if any(item == DEFAULT_MARK for item in row):
                is_full = False
                break
        return is_full
        
