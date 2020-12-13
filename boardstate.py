from constants import *


class Boardstate:
    '''A class with board, next_turn, is_game_over, and everything that
    we need to know about current state'''

    DEBUG_MODE = False
    
    def __init__(self, n):
        self.n = n
        self.board = [[SPACE] * n for i in range(n)]
        self.add_middle_pieces()
        self.next_turn = BLACK
        self.is_game_over = False
        self.winner = None
        self.num_pieces = 4 # board's initialized with 4 pieces
        self.last_turn_passed = False
        
    def add_middle_pieces(self):
        mid_x = (self.n - 1) // 2
        mid_y = mid_x
        self.board[mid_x][mid_y] = BLACK
        self.board[mid_x][mid_y + 1] = WHITE
        self.board[mid_x + 1][mid_y] = WHITE
        self.board[mid_x + 1][mid_y + 1] = BLACK

    def get_piece_count(self):
        b = 0
        w = 0
        for r in self.board:
            for c in r:
                if c == BLACK: b += 1
                elif c == WHITE: w += 1
        return b, w

    def update_winner(self):
        b, w = self.get_piece_count()
        if b > w:
            self.winner = BLACK
        elif w > b:
            self.winner = WHITE
        else:
            self.winner = SPACE # draw
        return
    
    def make_move(self, move):
        if move == (-1, -1):
            self.next_turn = BLACK if self.next_turn == WHITE else WHITE
            if self.last_turn_passed:
                self.is_game_over = True
                self.update_winner()
            else:
                self.last_turn_passed = True
        else:
            self.board[move[0]][move[1]] = self.next_turn
            self.next_turn = BLACK if self.next_turn == WHITE else WHITE
            self.num_pieces += 1
            self.last_turn_passed = False
            if self.num_pieces == self.n * self.n:
                self.is_game_over = True
                self.update_winner()
                
    def __str__(self):
        s = ""
        if Boardstate.DEBUG_MODE:
            s += "n: " + str(self.n) + '\n'
            s += "next_turn: "
            if self.next_turn == BLACK:
                s += "Black"
            else:
                s += "White"
            s += '\n'
            s += "is_game_over: " + str(self.is_game_over) + '\n'
            s += "winner: "
            if self.winner == BLACK:
                s += "Black"
            elif self.winner == WHITE:
                s += "White"
            else:
                s += "None"
            s += '\n'
        s += ' '
        for i in range(self.n):
            s += ' ' + str(i)
        s += '\n'
        s += ' '
        for _ in range(self.n):
            s += '--'
        s += '-\n'
        i = 0
        for r in self.board:
            s += str(i)
            i += 1
            for c in r:
                s += '|'
                if c == BLACK:
                    s += 'B'
                elif c == WHITE:
                    s += 'W'
                else:
                    s += ' '
            s += '|'
            s += '\n'
            s += ' '
            for _ in range(self.n):
                s += '--'
            s += '-\n'
        return s
