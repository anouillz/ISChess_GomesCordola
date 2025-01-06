import random
import time

from Bots.pieces_movements import apply_move, generate_moves


import numpy as np
#
#   Example function to be implemented for
#       Single important function is next_best
#           color: a single character str indicating the color represented by this bot ('w' for white)
#           board: a 2d matrix containing strings as a descriptors of the board '' means empty location "XC" means a piece represented by X of the color C is present there
#           budget: time budget allowed for this turn, the function must return a pair (xs,ys) --> (xd,yd) to indicate a piece at xs, ys moving to xd, yd
#

#   Be careful with modules to import from the root (don't forget the Bots.)
from Bots.ChessBotList import register_chess_bot

#   Simply move the pawns forward and tries to capture as soon as possible


import time

def generic_bot(player_sequence, board, time_budget, evaluate_board):
    color_sign = 1 if player_sequence[1] == 'w' else -1
    B = [[0 for _ in range(8)] for _ in range(8)]

    # Conversion du plateau en entiers
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

    # Initialization
    best_move = None
    max_depth = 100
    alpha = -float('inf')
    beta = float('inf')
    start_time = time.time()
    time_limit = time_budget - 0.1

    def iterative_deepening(board, max_depth, alpha, beta, start_time, time_limit):
        nonlocal best_move
        for depth in range(1, max_depth + 1):
            if time.time() - start_time > time_limit:
                break
            try:
                best_move = None
                max_eval = -float('inf')
                moves = generate_moves_with_king_priority(board, color_sign)
                for move in moves:
                    new_board = apply_move(board, move)
                    if abs(new_board[move[2]][move[3]]) == 5 * -color_sign:  # King capture
                        return move  # Immediate return for king capture
                    eval_score = minimax(new_board, depth - 1, alpha, beta, False, color_sign, evaluate_board, start_time, time_limit)
                    if eval_score > max_eval:
                        max_eval = eval_score
                        best_move = move
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break
            except TimeoutError:
                break
        return best_move

    # Call iterative deepening
    move = iterative_deepening(B, max_depth, alpha, beta, start_time, time_limit)

    if move:
        x1, y1, x2, y2 = move
        return (x1, y1), (x2, y2)
    else:
        return None

def generate_moves_with_king_priority(board, color_sign):
    """
    Generate moves and prioritize moves targeting the enemy king.
    """
    moves = generate_moves(board, color_sign)
    king_capture_moves = [move for move in moves if abs(board[move[2]][move[3]]) == 5 * -color_sign]
    if king_capture_moves:
        return king_capture_moves  # Return only moves that capture the enemy king
    return moves

def chess_bot_simple(player_sequence, board, time_budget, **kwargs):
    color_sign = 1 if player_sequence[1] == 'w' else -1
    return generic_bot(player_sequence, board, time_budget, evaluate_board_simple)

def chess_bot_advanced(player_sequence, board, time_budget, **kwargs):
    color_sign = 1 if player_sequence[1] == 'w' else -1
    return generic_bot(player_sequence, board, time_budget, evaluate_board_advanced)

def kingprotect(player_sequence, board, time_budget, **kwargs):
    color_sign = 1 if player_sequence[1] == 'w' else -1
    return generic_bot(player_sequence, board, time_budget, evaluate_board_kingProtection)

def kingprotect_with_center(player_sequence, board, time_budget, **kwargs):
    color_sign = 1 if player_sequence[1] == 'w' else -1
    return generic_bot(player_sequence, board, time_budget, evaluate_board_kingProtection_withCenter)

def pawnAligned_with_center(player_sequence, board, time_budget, **kwargs):
    color_sign = 1 if player_sequence[1] == 'w' else -1
    return generic_bot(player_sequence, board, time_budget, evaluate_board_pawnAligned_withCenter)

def pawnAligned(player_sequence, board, time_budget, **kwargs):
    color_sign = 1 if player_sequence[1] == 'w' else -1897894942863667242
    return generic_bot(player_sequence, board, time_budget, evaluate_board_pawnAligned)






def minimax(board, depth, alpha, beta, maximizing_player, color_sign, evaluate_board, start_time, time_limit):
    """
    Minimax algorithm with alpha-beta pruning.
    Incorporates the capture heuristic and king capture logic.
    """
    if time.time() - start_time > time_limit:
        return evaluate_board(board, color_sign)

    if depth == 0:
        return evaluate_board(board, color_sign)

    if maximizing_player:
        max_eval = -float('inf')
        for move in generate_moves_with_king_priority(board, color_sign):
            new_board = apply_move(board, move)
            if abs(new_board[move[2]][move[3]]) == 5 * -color_sign:  # Immediate king capture
                return float('inf')  # Immediate win
            eval_score = minimax(new_board, depth - 1, alpha, beta, False, color_sign, evaluate_board, start_time, time_limit)
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in generate_moves_with_king_priority(board, -color_sign):
            new_board = apply_move(board, move)
            if abs(new_board[move[2]][move[3]]) == 5 * color_sign:  # Immediate king capture by the opponent
                return -float('inf')  # Immediate loss
            eval_score = minimax(new_board, depth - 1, alpha, beta, True, color_sign, evaluate_board, start_time, time_limit)
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval


# Eval différente des board
def evaluate_board_simple(Bo, color_sign):
    piece_values = {
        1: 5,    # Tour
        2: 3,    # Cavalier
        3: 3,    # Fou
        4: 9,    # Reine
        5: 1000, # Roi
        6: 1     # Pion
    }

    score = 0
    for x in range(8):
        for y in range(8):
            piece = Bo[x][y]
            if piece != 0:
                value = piece_values[abs(piece)]
                if piece * color_sign > 0:
                    score += value
                else:
                    score -= value
    return score

def evaluate_board_kingProtection(Bo, color_sign, move_history=None, board_history=None):
    piece_values = {
        1: 500,  # Tour
        2: 300,  # Cavalier
        3: 300,  # Fou
        4: 900,  # Reine
        5: 10000,  # Roi
        6: 100  # Pion
    }

    MATE_SCORE = 100000  # Score très élevé pour le mat
    score = 0

    # Détection des positions terminales
    if is_checkmate(color_sign, Bo):  # Mat contre l'adversaire
        return MATE_SCORE
    if is_checkmate(-color_sign, Bo):  # Mat contre nous
        return -MATE_SCORE

    # Sécurité du roi
    if heuristic_king_safe(Bo, color_sign):
        score += 100  # Bonus pour un roi en sécurité

    moves = generate_moves(Bo, color_sign)
    mobility_score = len(moves) * 10  # Chaque coup disponible vaut 10 centipions
    score += mobility_score

    # Apply capture heuristic
    capture_score = evaluate_capture_heuristic(Bo, color_sign, piece_values)
    score += capture_score

    # Réduction des scores répétés
    if board_history:
        score += detect_repetition(Bo, board_history)

    if color_sign == 1:
        print("white score = ", score)
    else:
        print("black score = ", score)

    return score

def evaluate_board_kingProtection_withCenter(Bo, color_sign, move_history=None, board_history=None):
    piece_values = {
        1: 500,  # Tour
        2: 300,  # Cavalier
        3: 300,  # Fou
        4: 900,  # Reine
        5: 10000,  # Roi
        6: 100  # Pion
    }

    MATE_SCORE = 100000  # Score très élevé pour le mat
    score = 0

    # Détection des positions terminales
    if is_checkmate(color_sign, Bo):  # Mat contre l'adversaire
        return MATE_SCORE
    if is_checkmate(-color_sign, Bo):  # Mat contre nous
        return -MATE_SCORE

    board_center_score = heuristic_board_center(Bo, color_sign)
    score += board_center_score

    # Sécurité du roi
    if heuristic_king_safe(Bo, color_sign):
        score += 100  # Bonus pour un roi en sécurité

    moves = generate_moves(Bo, color_sign)
    mobility_score = len(moves) * 10  # Chaque coup disponible vaut 10 centipions
    score += mobility_score

    # Apply capture heuristic
    capture_score = evaluate_capture_heuristic(Bo, color_sign, piece_values)
    score += capture_score


    # Réduction des scores répétés
    if board_history:
        score += detect_repetition(Bo, board_history)

    if color_sign == 1:
        print("white score = ", score)
    else:
        print("black score = ", score)

    return score

def evaluate_board_pawnAligned_withCenter(Bo, color_sign, move_history=None, board_history=None):
    piece_values = {
        1: 500,  # Tour
        2: 300,  # Cavalier
        3: 300,  # Fou
        4: 900,  # Reine
        5: 10000,  # Roi
        6: 100  # Pion
    }

    MATE_SCORE = 100000  # Score très élevé pour le mat
    score = 0

    # Détection des positions terminales
    if is_checkmate(color_sign, Bo):  # Mat contre l'adversaire
        return MATE_SCORE
    if is_checkmate(-color_sign, Bo):  # Mat contre nous
        return -MATE_SCORE

    board_center_score = heuristic_board_center(Bo, color_sign)
    score += board_center_score

    # pawn aligned
    pawn_aligned_score = heuristic_pawn_aligned(Bo, color_sign)
    score += pawn_aligned_score

    # Apply capture heuristic
    capture_score = evaluate_capture_heuristic(Bo, color_sign, piece_values)
    score += capture_score

    moves = generate_moves(Bo, color_sign)
    mobility_score = len(moves) * 10  # Chaque coup disponible vaut 10 centipions
    score += mobility_score

    # Réduction des scores répétés
    if board_history:
        score += detect_repetition(Bo, board_history)

    if color_sign == 1:
        print("white score = ", score)
    else:
        print("black score = ", score)

    return score

def evaluate_board_pawnAligned(Bo, color_sign, move_history=None, board_history=None):
    piece_values = {
        1: 500,  # Tour
        2: 300,  # Cavalier
        3: 300,  # Fou
        4: 900,  # Reine
        5: 10000,  # Roi
        6: 100  # Pion
    }

    MATE_SCORE = 100000  # Score très élevé pour le mat
    score = 0

    # Détection des positions terminales
    if is_checkmate(color_sign, Bo):  # Mat contre l'adversaire
        return MATE_SCORE
    if is_checkmate(-color_sign, Bo):  # Mat contre nous
        return -MATE_SCORE

    # pawn aligned
    pawn_aligned_score = heuristic_pawn_aligned(Bo, color_sign)
    score += pawn_aligned_score

    # Apply capture heuristic
    capture_score = evaluate_capture_heuristic(Bo, color_sign, piece_values)
    score += capture_score

    moves = generate_moves(Bo, color_sign)
    mobility_score = len(moves) * 10  # Chaque coup disponible vaut 10 centipions
    score += mobility_score

    # Réduction des scores répétés
    if board_history:
        score += detect_repetition(Bo, board_history)

    if color_sign == 1:
        print("white score = ", score)
    else:
        print("black score = ", score)

    return score

def evaluate_board_advanced(Bo, color_sign, move_history=None, board_history=None):
    """
    Évaluation avancée inspirée du site "Score" de Chess Programming.
    """
    piece_values = {
        1: 500,    # Tour
        2: 300,    # Cavalier
        3: 300,    # Fou
        4: 900,    # Reine
        5: 10000,  # Roi
        6: 100     # Pion
    }

    MATE_SCORE = 6666000000  # Score très élevé pour le mat

    #DRAW_SCORE = 0       # Score neutre pour les nulles
    #CONTEMPT_FACTOR = 10 # Facteur de mépris pour éviter les nulles

    # Détection des positions terminales
    if is_checkmate(color_sign, Bo):  # Mat contre l'adversaire
        return MATE_SCORE
    if is_checkmate(-color_sign, Bo):  # Mat contre nous
        return -MATE_SCORE

    # Score heuristique initial
    score = 0

    # Valeur matérielle
    for x in range(8):
        for y in range(8):
            piece = Bo[x][y]
            if piece != 0:
                value = piece_values[abs(piece)]
                score += value if piece * color_sign > 0 else -value

    # Contrôle du centre
    board_center_score = heuristic_board_center(Bo, color_sign)
    score += board_center_score

    # Apply capture heuristic
    capture_score = evaluate_capture_heuristic(Bo, color_sign, piece_values)
    score += capture_score

    # Mobilité
    moves = generate_moves(Bo, color_sign)
    mobility_score = len(moves) * 10  # Chaque coup disponible vaut 10 centipions
    score += mobility_score

    # Sécurité du roi
    if heuristic_king_safe(Bo, color_sign):
        score += 100  # Bonus pour un roi en sécurité

    # Structure de pions
    pawn_aligned_score = heuristic_pawn_aligned(Bo, color_sign)
    score += pawn_aligned_score

    # Réduction des scores répétés
    if board_history:
        score += detect_repetition(Bo, board_history)

    if color_sign == 1:
        print("white score = ", score)
    else:
        print("black score = ", score)

    return score





# fonction pour les eval
def penalize_repeated_moves(move, move_history):
    if move in move_history:
        return -0.5  # Pénalité pour un mouvement répété
    return 0
#heuristic for king protection
def get_king_position(board, color_sign):
    # Trouve la position du roi
    king_position = None
    for x in range(8):
        for y in range(8):
            if board[x][y] == 5 * color_sign:  # Roi de la couleur donnée
                king_position = (x, y)
                break
    if not king_position:
        return False  # Aucun roi trouvé (cas improbable)
    return king_position

def heuristic_king_protect(board, color_sign):
    """
    Vérifie si le roi est en échec.
    :param Bo: Plateau actuel.
    :param color_sign: +1 pour les blancs, -1 pour les noirs.
    :return: True si le roi est en échec, False sinon.
    """

    x,y = get_king_position(board, color_sign)

    # Menaces des pions
    pawn_directions = [(-1, -1), (-1, 1)] if color_sign == 1 else [(1, -1), (1, 1)]
    for dx, dy in pawn_directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 8 and 0 <= ny < 8 and board[nx][ny] == -6 * color_sign:
            return True

    # Menaces des cavaliers
    knight_moves = [
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
    ]
    for dx, dy in knight_moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 8 and 0 <= ny < 8 and board[nx][ny] == -2 * color_sign:
            return True

    # Menaces des fous et de la reine (diagonales)
    bishop_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dx, dy in bishop_directions:
        nx, ny = x, y
        while True:
            nx += dx
            ny += dy
            if not (0 <= nx < 8 and 0 <= ny < 8):
                break
            if board[nx][ny] == -3 * color_sign or board[nx][ny] == -4 * color_sign:
                return True
            if board[nx][ny] != 0:  # Collision avec une pièce
                break

    # Menaces des tours et de la reine (lignes et colonnes)
    rook_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in rook_directions:
        nx, ny = x, y
        while True:
            nx += dx
            ny += dy
            if not (0 <= nx < 8 and 0 <= ny < 8):
                break
            if board[nx][ny] == -1 * color_sign or board[nx][ny] == -4 * color_sign:
                return True
            if board[nx][ny] != 0:  # Collision avec une pièce
                break

    # Menaces du roi adverse
    king_moves = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    for dx, dy in king_moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 8 and 0 <= ny < 8 and board[nx][ny] == -5 * color_sign:
            return True

    # Si aucune menace détectée
    return False


def is_checkmate(color_sign, board):
    """
    Vérifie si le joueur est en échec et mat.
    :param color_sign: +1 pour les blancs, -1 pour les noirs.
    :param Bo: Plateau.
    :return: True si le joueur est en échec et mat, False sinon.
    """
    moves = generate_moves(board, color_sign)
    if not moves and heuristic_king_protect(board, color_sign):
        return True
    return False
def heuristic_king_safe(Bo, color_sign):
    """
    Vérifie si le roi est en sécurité.
    :param color_sign: +1 pour les blancs, -1 pour les noirs.
    :param Bo: Plateau.
    :return: True si le roi est en sécurité, False sinon.
    """
    king_position = None
    for x in range(8):
        for y in range(8):
            if Bo[x][y] == 5 * color_sign:  # Trouve la position du roi
                king_position = (x, y)
                break
    if not king_position:
        return False  # Roi inexistant (cas rare)

    return not heuristic_king_protect(Bo, color_sign)

#heuristic for pawn aligned
def is_pawn_passed(x, y, Bo, color_sign):
    """
    Vérifie si un pion est passé.
    :param x: Coordonnée x du pion.
    :param y: Coordonnée y du pion.
    :param Bo: Plateau.
    :param color_sign: +1 pour les blancs, -1 pour les noirs.
    :return: True si le pion est passé, False sinon.
    """
    direction = 1 if color_sign == 1 else -1
    for nx in range(x + direction, 8 if color_sign == 1 else -1, direction):
        for dy in [-1, 0, 1]:
            ny = y + dy
            if 0 <= ny < 8 and Bo[nx][ny] * color_sign < 0 and abs(Bo[nx][ny]) == 6:
                return False  # Pion adverse peut bloquer ou capturer
    return True
def is_pawn_protected(x, y, Bo, color_sign):
    """
    Vérifie si un pion est protégé par un autre pion.
    :param x: Coordonnée x du pion.
    :param y: Coordonnée y du pion.
    :param Bo: Plateau.
    :param color_sign: +1 pour les blancs, -1 pour les noirs.
    :return: True si le pion est protégé, False sinon.
    """
    for dx, dy in [(1, -1), (1, 1)] if color_sign == 1 else [(-1, -1), (-1, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 8 and 0 <= ny < 8 and Bo[nx][ny] == 6 * color_sign:
            return True
    return False
def is_pawn_isolated(x, y, Bo):
    """
    Vérifie si un pion est isolé.
    :param x: Coordonnée x du pion.
    :param y: Coordonnée y du pion.
    :param Bo: Plateau.
    :return: True si le pion est isolé, False sinon.
    """
    for dy in [-1, 1]:  # Colonnes adjacentes
        ny = y + dy
        if 0 <= ny < 8:
            for nx in range(8):  # Vérifie toute la colonne adjacente
                if Bo[nx][ny] == Bo[x][y]:
                    return False
    return True
def heuristic_pawn_aligned(board, color_sign):
    for x in range(8):
        for y in range(8):
            piece = board[x][y]
            if abs(piece) == 6:  # Pion
                if piece * color_sign > 0:
                    # Bonus pour pions passés ou protégés
                    if is_pawn_passed(x, y, board, color_sign):
                        return 50
                    if is_pawn_protected(x, y, board, color_sign):
                        return 30
                    # Pénalité pour pions isolés ou doublés
                    if is_pawn_isolated(x, y, board):
                        return -30
    return 0


#heuristic for board center control
#get total nb of pieces in the board
def get_nb_pieces(board):
    count = 0
    for x in range(len(board)):
        for y in range(len(board)):
            if board[x][y] != 0:
                count += 1
    return count
def heuristic_board_center(board, color_sign):
    #center_positions = [(3, 3), (3, 4), (4, 3), (4, 4)]
    center_positions = [(2,2),(2,3),(2,4),(2,5),(3,2),(3,5),(4,2),(4,5),(5,2),(5,3),(5,4),(5,5)]

    if get_nb_pieces(board) > 29:
        for x, y in center_positions:
            piece = board[x][y]
            if piece * color_sign > 0:  # Pièce alliée au centre
                return 50  # Bonus pour contrôler le centre
            elif piece * color_sign < 0:  # Pièce ennemie au centre
                return -50  # Malus si l'adversaire contrôle le centre

    return 0


#checks if a move has been repeated
def detect_repetition(Bo, board_history):
    """
    Vérifie si une position a été répétée plus de deux fois.
    :param Bo: Plateau actuel.
    :param board_history: Historique des plateaux.
    :return: -5 si une répétition est détectée, 0 sinon.
    """
    count = board_history.count(Bo)
    if count > 2:
        return -5  # Pénalité pour répétition
    return 0

def evaluate_capture_heuristic(board, color_sign, piece_values):
    """
    Heuristic to prioritize capturing higher-value pieces with lower-value pieces.
    """
    capture_score = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] * color_sign > 0:  # Player's pieces
                moves = generate_moves(board, color_sign)
                for move in moves:
                    target_piece = board[move[2]][move[3]]
                    if target_piece * -color_sign > 0:  # Enemy piece
                        capture_score += abs(piece_values[abs(target_piece)]) - abs(piece_values[abs(board[move[0]][move[1]])])
    return capture_score


#   Example how to register the function
# register_chess_bot("simple", chess_bot_simple)
register_chess_bot("2advanced", chess_bot_advanced)
register_chess_bot("2kingprotect", kingprotect)
register_chess_bot("2kingprotect_with_center", kingprotect_with_center)
register_chess_bot("2pawnAligned_with_center", pawnAligned_with_center)
register_chess_bot("2pawnAligned", pawnAligned)

