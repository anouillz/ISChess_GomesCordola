
from Bots.CGG_chess_piece_moves import generate_moves
from Bots.CGG_heuristics import heuristic_king_safe, heuristic_board_center, detect_repetition, capture_heuristic, heuristic_pawn_aligned, is_checkmate, capture_heuristic
from Bots.CGG import generic_bot

#board evaluation

# evaluate board functions
def evaluate_board_kingProtection(board, color_sign, move_history=None, board_history=None):
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

def evaluate_board_pawnAligned_withCenter(board, color_sign, move_history=None, board_history=None):
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

    # pawn aligned
    pawn_aligned_score = heuristic_pawn_aligned(board, color_sign)
    score += pawn_aligned_score

    # Apply capture heuristic
    capture_score = capture_heuristic(board, color_sign, piece_values)
    score += capture_score

    moves = generate_moves(board, color_sign)
    # mobility heuristic -- number of available moves
    mobility_score = len(moves) * 10
    score += mobility_score

    # reduce scores for repeated moves
    if board_history:
        score += detect_repetition(board, board_history)

    return score

def evaluate_board_pawnAligned(board, color_sign, move_history=None, board_history=None):
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

    # pawn aligned
    pawn_aligned_score = heuristic_pawn_aligned(board, color_sign)
    score += pawn_aligned_score

    # Apply capture heuristic
    capture_score = capture_heuristic(board, color_sign, piece_values)
    score += capture_score

    moves = generate_moves(board, color_sign)
    # mobility heuristic -- number of available moves
    mobility_score = len(moves) * 10
    score += mobility_score

    # reduce scores for repeated moves
    if board_history:
        score += detect_repetition(board, board_history)

    return score

def evaluate_board_advanced(board, color_sign, move_history=None, board_history=None):
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


    score = 0

    # points for each piece
    for x in range(8):
        for y in range(8):
            piece = board[x][y]
            if piece != 0:
                value = piece_values[abs(piece)]
                score += value if piece * color_sign > 0 else -value

    # center control
    board_center_score = heuristic_board_center(board, color_sign)
    score += board_center_score

    # Apply capture heuristic
    capture_score = capture_heuristic(board, color_sign, piece_values)
    score += capture_score


    moves = generate_moves(board, color_sign)
    # mobility heuristic -- number of available moves
    mobility_score = len(moves) * 10
    score += mobility_score

    # king safety
    if heuristic_king_safe(board, color_sign):
        score += 100  # Bonus pour un roi en sécurité

    # pawns aligned
    pawn_aligned_score = heuristic_pawn_aligned(board, color_sign)
    score += pawn_aligned_score

    # reduce scores for repeated moves
    if board_history:
        score += detect_repetition(board, board_history)

    return score


#bots
# generate moves with king priority: if a piece can capture the opponent's king, prioritize that move
def generate_moves_with_king_priority(board, color_sign):
    moves = generate_moves(board, color_sign)
    king_capture_moves = [move for move in moves if abs(board[move[2]][move[3]]) == 5 * -color_sign]

    if king_capture_moves:
        return king_capture_moves

    return moves

# bot with king protection, center control, pawn alignment -- not chosen for the tournament
def chess_bot_advanced(player_sequence, board, time_budget, **kwargs):
    color_sign = 1 if player_sequence[1] == 'w' else -1
    return generic_bot(player_sequence, board, time_budget, evaluate_board_advanced)

# bot with king protection heuristic -- not chosen for the tournament
def chess_bot_kingprotect(player_sequence, board, time_budget, **kwargs):
    color_sign = 1 if player_sequence[1] == 'w' else -1
    return generic_bot(player_sequence, board, time_budget, evaluate_board_kingProtection)

# bot with pawn alignment and center control -- not chosen for the tournament
def pawnAligned_with_center(player_sequence, board, time_budget, **kwargs):
    color_sign = 1 if player_sequence[1] == 'w' else -1
    return generic_bot(player_sequence, board, time_budget, evaluate_board_pawnAligned_withCenter)

# bot with pawn alignment -- not chosen for the tournament
def pawnAligned(player_sequence, board, time_budget, **kwargs):
    color_sign = 1 if player_sequence[1] == 'w' else -1897894942863667242
    return generic_bot(player_sequence, board, time_budget, evaluate_board_pawnAligned)