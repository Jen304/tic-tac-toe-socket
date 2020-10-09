DEFAULT_MARK= '_'

class Board: 
    def __init__(self, num_rows, num_cols):
        self.board = []
        self.rows = num_rows
        self.cols = num_cols
        for i in range(num_rows):
            new_row = [ DEFAULT_MARK for i in range(num_cols)]
            self.board.append(new_row)
        
    def mark(self, mark, row, col):
        if(self.board[row][col] != DEFAULT_MARK):
            raise Exception('Invalid')
        self.board[row][col] = mark

    def get_board_string(self):
        board_str = ''
        for row in self.board:
            board_str = board_str + ''.join([str(elem) + ' ' for elem in row]) + '\n'
        print(board_str)
        return board_str

    def check_winner(self):
        ''' Purpose: check the winner in the board
            Return the winner (symbol) or none
        '''
        winner = None
        winner = self.check_col()
        if(not winner):
            winner = self.check_row()
        if(not winner):
            winner = self.check_col()
        if(not winner):
            winner = self.check_diagonal_left_to_right()
        if(not winner):
            winner = self.check_diagonal_right_to_left()
        return winner

    def check_col(self):
        col = 0
        winner = None
        while col < self.cols:
            item = self.board[0][col]
            if(item == DEFAULT_MARK):
                col = col + 1
                continue
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
        winner = None
        for row in self.board:
            checking_item = row[0]
            if (checking_item == DEFAULT_MARK):
                continue
            if all(checking_item == item for item in row):
                winner = row[0]
                break
        return winner

    def check_diagonal_left_to_right(self):
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
        is_full = True
        for row in self.board:
            if any(item == DEFAULT_MARK for item in row):
                is_full = False
                break
        return is_full
        
