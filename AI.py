from copy import deepcopy
from boardstate import *

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
    
def AI(b_state, time):
    maximizer = BLACK
    max_depth = 5
    for depth in range(1, max_depth + 1):
        best_score, best_move = minimax(b_state, depth, NEG_INF, POS_INF, maximizer)
    return [best_score, best_move]

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
