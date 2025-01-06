
import time
from Bots.CGG_chess_piece_moves import apply_move, generate_moves
from Bots.ChessBotList import register_chess_bot
from Bots.CGG_heuristics import heuristic_king_safe, heuristic_board_center, detect_repetition, capture_heuristic, heuristic_pawn_aligned, is_checkmate




# generic bot method to be used by all bots
def generic_bot(player_sequence, board, time_budget, evaluate_board):
    color_sign = 1 if player_sequence[1] == 'w' else -1
    B = [[0 for _ in range(8)] for _ in range(8)]

    # Convert the board to a numerical representation
    for x in range(board.shape[0]):
        for y in range(board.shape[1]):
            match board[x][y]:
                case "rw": B[x][y] = 1
                case "nw": B[x][y] = 2
                case "bw": B[x][y] = 3
                case "qw": B[x][y] = 4
                case "kw": B[x][y] = 5
                case "pw": B[x][y] = 6
                case "rb": B[x][y] = -1
                case "nb": B[x][y] = -2
                case "bb": B[x][y] = -3
                case "qb": B[x][y] = -4
                case "kb": B[x][y] = -5
                case "pb": B[x][y] = -6
                case _: B[x][y] = 0


    # Find all moves
    moves = generate_moves(B, color_sign)

    # Check if any move captures the opponent's king
    for move in moves:
        start_x, start_y, end_x, end_y = move
        if abs(B[end_x][end_y]) == 5 * -color_sign:  # Opponent's king
            # Return the move immediately
            return (start_x, start_y), (end_x, end_y)

    # Initialization for search
    max_depth = 100
    alpha = -float('inf')
    beta = float('inf')
    best_move = None

    # Time for tests
    start_time = time.time()
    time_limit = time_budget - 0.1



    # Iterative deepening
    # important so that we can return the best move found so far
    def iterative_deepening(board, max_depth, alpha, beta, start_time, time_limit):
        nonlocal best_move

        for depth in range(1, max_depth + 1):
            # Break if time limit is reached and return the best move found so far
            if time.time() - start_time > time_limit:
                break
            try:
                best_move = None
                max_eval = -float('inf')
                moves = generate_moves(board, color_sign)
                for move in moves:
                    # apply move and evaluate
                    new_board = apply_move(board, move)
                    eval_score = minimax(new_board, depth - 1, alpha, beta, False, color_sign, evaluate_board, start_time, time_limit)
                    if eval_score > max_eval:
                        max_eval = eval_score
                        best_move = move
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        # if the current move is worse than the best move found so far, break
                        break
            except TimeoutError:
                break

        return best_move

    # Perform iterative deepening
    move = iterative_deepening(B, max_depth, alpha, beta, start_time, time_limit)

    # Return the best move found
    if move:
        start_x, start_y, end_x, end_y = move
        return (start_x, start_y), (end_x, end_y)
    else:
        return None


# bot with king protection and center control -- chosen for the tournament
def kingprotect_with_center(player_sequence, board, time_budget, **kwargs):
    color_sign = 1 if player_sequence[1] == 'w' else -1
    return generic_bot(player_sequence, board, time_budget, evaluate_board_kingProtection_withCenter)

# Minimax algorithm with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizing_player, color_sign, evaluate_board, start_time, time_limit):
    # Break if time limit is reached
    if time.time() - start_time > time_limit:
        return evaluate_board(board, color_sign)

    if depth == 0:
        return evaluate_board(board, color_sign)

    # we want maximizing player to be the player that wins
    if maximizing_player:
        max_eval = -float('inf')
        for move in generate_moves(board, color_sign):
            new_board = apply_move(board, move)
            if abs(new_board[move[2]][move[3]]) == 5 * -color_sign:  # Immediate king capture
                return float('inf')  # Immediate win
            eval_score = minimax(new_board, depth - 1, alpha, beta, False, color_sign, evaluate_board, start_time, time_limit)
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                # if the current move is worse than the best move found so far
                break
        return max_eval
    # minimizing player, we want it to be the player that loses
    else:
        min_eval = float('inf')
        for move in generate_moves(board, -color_sign):
            new_board = apply_move(board, move)
            if abs(new_board[move[2]][move[3]]) == 5 * color_sign:  # Immediate king capture by the opponent
                return -float('inf')  # Immediate loss
            eval_score = minimax(new_board, depth - 1, alpha, beta, True, color_sign, evaluate_board, start_time, time_limit)
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval






def evaluate_board_kingProtection_withCenter(board, color_sign, move_history=None, board_history=None):
    piece_values = {
        1: 500,  # rook
        2: 300,  # knight
        3: 300,  # bishop
        4: 900,  # queen
        5: 10000,  # king
        6: 100  # pawn
    }

    MATE_SCORE = 100000  # high score for checkmate
    score = 0

    # check for terminal positions
    if is_checkmate(color_sign, board):  # checkmate against the opponent
        return MATE_SCORE
    if is_checkmate(-color_sign, board):  # checkmate against us
        return -MATE_SCORE

    # center control
    board_center_score = heuristic_board_center(board, color_sign)
    score += board_center_score

    # king safety
    if heuristic_king_safe(board, color_sign):
        score += 100  # bonus for a safe king

    moves = generate_moves(board, color_sign)
    # mobility heuristic -- number of available moves
    mobility_score = len(moves) * 10
    score += mobility_score

    # Apply capture heuristic
    capture_score = capture_heuristic(board, color_sign, piece_values)
    score += capture_score


    # reduce scores for repeated moves
    if board_history:
        score += detect_repetition(board, board_history)


    return score




register_chess_bot("CGG", kingprotect_with_center)

