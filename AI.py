from copy import deepcopy
import time

current_milli_time = lambda: int(round(time.time() * 1000))

SPACE = ' '
BLACK = 'B'
WHITE = 'W'
NEG_INF = -10000000000
POS_INF = 10000000000

class Boardstate:
    '''A class with board, next_turn, is_game_over, and everything that
    we need to know about current state'''

    DEBUG_MODE = False
    
    def __init__(self, n, board=None, next_turn=None):
        self.n = n
        if board == None:
            self.board = [[SPACE] * n for i in range(n)]
            self.add_middle_pieces()
        else:
            self.board = board
        self.next_turn = BLACK if next_turn = None else next_turn
        self.is_game_over = False
        self.winner = None
        self.num_pieces = 4 # board's initialized with 4 pieces
        self.last_turn_passed = False

    def __init
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


def copy_b_state(b_state):
    new_b_state = Boardstate(b_state.n)
    new_b_state.next_turn = b_state.next_turn
    new_b_state.is_game_over = b_state.is_game_over
    new_b_state.winner = b_state.winner
    new_b_state.board = deepcopy(b_state.board)
    new_b_state.num_pieces = b_state.num_pieces
    new_b_state.last_turn_passed = b_state.last_turn_passed
    return new_b_state


def heuristics(b_state):
    b, w = b_state.get_piece_count()
        return b - w

def minimax(b_state, depth_left, alpha, beta, maximizer):
    if depth_left == 0 or b_state.is_game_over:
        return heuristics(b_state), None
    if b_state.next_turn == maximizer:
        maximum = NEG_INF
        arg_max = None
        move_found = False
        for r in range(b_state.n):
            for c in range(b_state.n):
                new_state, is_valid = get_next_state(b_state, (r, c))
                if is_valid:
                    move_found = True
                    score, move = minimax(new_state, depth_left - 1, alpha, beta, maximizer)
                    alpha = max(alpha, score)
                    if score > maximum:
                        maximum = score
                        arg_max = (r, c)
                    if beta <= alpha:
                        break
        if not move_found:
            new_state, is_valid = get_next_state(b_state, (-1, -1))
            score, move = minimax(new_state, depth_left - 1, alpha, beta, maximizer)
            return score, (-1, -1)
        return maximum, arg_max
    else:
        minimum = POS_INF
        arg_min = None
        move_found = False
        for r in range(b_state.n):
            for c in range(b_state.n):
                new_state, is_valid = get_next_state(b_state, (r, c))
                if is_valid:
                    move_found = True
                    score, move = minimax(new_state, depth_left - 1, alpha, beta, maximizer)
                    beta = min(score, beta)
                    if score < minimum:
                        minimum = score
                        arg_min = (r, c)
                    if beta <= alpha:
                        break
        if not move_found:
            new_state, is_valid = get_next_state(b_state, (-1, -1))
            score, move = minimax(new_state, depth_left - 1, alpha, beta, maximizer)
            return score, (-1, -1)
        return minimum, arg_min
    
def get_move(board_size, board_state, turn, time_left, opponent_time_left):
    start_time = current_milli_time
    maximizer = BLACK
    max_depth = 4
    best_score = NEG_INF if turn == BLACK else POS_INF
    best_move = None
    b_state = Boardstate(board_size, board_state, turn)
    while current_milli_time - start_time < 4500:
        c_b_state = copy_b_state(b_state) 
        b_score, b_move = minimax(c_b_state, max_depth, NEG_INF, POS_INF, maximizer)
        if turn == maximizer:
            if b_score > best_score:
                best_score = b_score
                best_move = b_move
        else:
            if b_score < best_score:
                best_score = b_score
                best_move = b_move
        
    if best_move == (-1, -1): best_move = None
    return best_move

def outofbounds(n, r, c):
    return r < 0 or c < 0 or r >= n or c >=n

def is_capture(b_state, next_move, direction):
    next_r = next_move[0] + direction[0]
    next_c = next_move[1] + direction[1]
    if outofbounds(b_state.n, next_r, next_c) or b_state.board[next_r][next_c] == b_state.next_turn \
       or b_state.board[next_r][next_c] == SPACE:
        return False
    next_r = next_r + direction[0]
    next_c = next_c + direction[1]
    while not outofbounds(b_state.n, next_r, next_c):
        if b_state.board[next_r][next_c] == b_state.next_turn:
            return True
        if b_state.board[next_r][next_c] == SPACE:
            return False
        next_r = next_r + direction[0]
        next_c = next_c + direction[1]
    return False

def capture(b_state, next_move, direction):
    next_r = next_move[0] + direction[0]
    next_c = next_move[1] + direction[1]
    while b_state.board[next_r][next_c] != b_state.next_turn:
        b_state.board[next_r][next_c] = b_state.next_turn
        next_r = next_r + direction[0]
        next_c = next_c + direction[1]
    return

def get_next_state(board_state, next_move):
    b_state = copy_b_state(board_state)
    if next_move == (-1, -1):
        b_state.make_move(next_move)
        return b_state, True
    
    if b_state.board[next_move[0]][next_move[1]] != SPACE:
        return b_state, False
    d = [-1, 0, 1]
    captured = False
    for dx in d:
        for dy in d:
            if dx != 0 or dy != 0:
                if is_capture(b_state, next_move, (dx, dy)):
                    captured = True
                    capture(b_state, next_move, (dx, dy))
    if capture:
         b_state.make_move(next_move)
    return b_state, captured
