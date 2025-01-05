import random
import time

import numpy as np
#
#   Example function to be implemented for
#       Single important function is next_best
#           color: a single character str indicating the color represented by this bot ('w' for white)
#           board: a 2d matrix containing strings as a descriptors of the board '' means empty location "XC" means a piece represented by X of the color C is present there
#           budget: time budget allowed for this turn, the function must return a pair (xs,ys) --> (xd,yd) to indicate a piece at xs, ys moving to xd, yd
#

from PyQt6 import QtCore
from collections import deque
#   Be careful with modules to import from the root (don't forget the Bots.)
from Bots.ChessBotList import register_chess_bot

#   Simply move the pawns forward and tries to capture as soon as possible


import time

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

    # Initialisation
    best_move = None
    max_depth = 100  # Profondeur maximale arbitraire
    alpha = -float('inf')
    beta = float('inf')
    start_time = time.time()
    time_limit = time_budget - 0.1  # Petite marge pour éviter de dépasser le temps

    def iterative_deepening(Bo, max_depth, alpha, beta, start_time, time_limit):
        nonlocal best_move
        for depth in range(1, max_depth + 1):
            if time.time() - start_time > time_limit:
                break  # Temps écoulé, on s'arrête
            try:
                best_move = None
                max_eval = -float('inf')
                moves = generer_deplacements(Bo, color_sign)
                for move in moves:
                    new_board = appliquer_deplacement(Bo, move)
                    eval = minimax(new_board, depth - 1, alpha, beta, False, color_sign, evaluate_board, start_time, time_limit)
                    if eval > max_eval:
                        max_eval = eval
                        best_move = move
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break  # Coupe bêta
            except TimeoutError:
                break  # Si une limite de temps est atteinte dans minimax
        return best_move

    # Appel d'Iterative Deepening
    move = iterative_deepening(B, max_depth, alpha, beta, start_time, time_limit)

    if move:
        x1, y1, x2, y2 = move
        return (x1, y1), (x2, y2)
    else:
        return None


def chess_bot_simple(player_sequence, board, time_budget, **kwargs):
    color_sign = 1 if player_sequence[1] == 'w' else -1
    return generic_bot(player_sequence, board, time_budget, evaluate_board_simple)

def chess_bot_advanced(player_sequence, board, time_budget, **kwargs):
    color_sign = 1 if player_sequence[1] == 'w' else -1
    return generic_bot(player_sequence, board, time_budget, evaluate_board_advanced)


def cavalier(pos_x, pos_y, Bo, color_sign):
    mouvements = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]
    deplacements = []
    for dx, dy in mouvements:
        nx, ny = pos_x + dx, pos_y + dy
        if 0 <= nx <= 7 and 0 <= ny <= 7:
            piece = Bo[nx][ny]
            if piece == 0 or (piece * color_sign < 0):  # Vide ou pièce ennemie
                deplacements.append((nx, ny))
    return deplacements

def pion(pos_x, pos_y, Bo, color_sign):
    deplacements = []
    direction = 1

    # Avance simple
    nx = pos_x + direction
    if 0 <= nx <= 7 and Bo[nx][pos_y] == 0:  # La case devant est vide
        deplacements.append((nx, pos_y))

    # Captures diagonales
    for dy in [-1, 1]:
        nx, ny = pos_x + direction, pos_y + dy
        if 0 <= nx <= 7 and 0 <= ny <= 7:
            if Bo[nx][ny] * color_sign < 0:  # Pièce ennemie
                deplacements.append((nx, ny))

    return deplacements

def roi(pos_x, pos_y, Bo, color_sign):
    mouvements = [
        (-1, -1), (-1, 0), (-1, 1),  # Haut gauche, haut, haut droite
        (0, -1),          (0, 1),   # Gauche, droite
        (1, -1), (1, 0), (1, 1)     # Bas gauche, bas, bas droite
    ]
    deplacements = []

    for dx, dy in mouvements:
        nx, ny = pos_x + dx, pos_y + dy
        if 0 <= nx <= 7 and 0 <= ny <= 7:  # Vérifie que la position reste sur le plateau
            piece = Bo[nx][ny]
            if piece == 0 or piece * color_sign < 0:  # Case vide ou occupée par une pièce ennemie
                deplacements.append((nx, ny))

    return deplacements

def tour(pos_x, pos_y, Bo, color_sign):
    """
    Génère les déplacements possibles pour une tour.
    """
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Haut, Bas, Gauche, Droite
    return get_moves_directions(Bo, pos_x, pos_y, color_sign, directions)

def fou(pos_x, pos_y, Bo, color_sign):
    """
    Génère les déplacements possibles pour un fou.
    """
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonales
    return get_moves_directions(Bo, pos_x, pos_y, color_sign, directions)

def reine(pos_x, pos_y, Bo, color_sign):
    """
    Génère les déplacements possibles pour une reine.
    """
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),  # Directions de la tour
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # Directions du fou
    ]
    return get_moves_directions(Bo, pos_x, pos_y, color_sign, directions)

def get_moves_directions(Bo, pos_x, pos_y, color_sign, directions):
    """
    Génère les déplacements possibles dans les directions spécifiées.
    """
    moves = []
    for dx, dy in directions:
        nx, ny = pos_x + dx, pos_y + dy
        while 0 <= nx < 8 and 0 <= ny < 8:
            piece = Bo[nx][ny]
            if piece == 0:  # Case vide
                moves.append((nx, ny))
            elif piece * color_sign < 0:  # Pièce ennemie
                moves.append((nx, ny))
                break
            else:  # Pièce alliée
                break
            nx += dx
            ny += dy
    return moves

# Déplacement des pièces
def appliquer_deplacement(Bo, move):
    x1, y1, x2, y2 = move
    new_board = [row[:] for row in Bo]  # Copie profonde du plateau
    new_board[x2][y2] = new_board[x1][y1]
    new_board[x1][y1] = 0
    return new_board


def generer_deplacements(Bo, color_sign):
    """
    Génère tous les déplacements possibles pour un joueur donné.
    :param Bo: Plateau
    :param color_sign: +1 pour les blancs, -1 pour les noirs
    :return: Liste des déplacements possibles
    """
    deplacements = []
    for x in range(8):
        for y in range(8):
            piece = Bo[x][y]
            if piece * color_sign > 0:  # Pièce alliée
                if abs(piece) == 6:  # Pion
                    moves = pion(x, y, Bo, color_sign)
                    deplacements.extend([(x, y, nx, ny) for nx, ny in moves])
                elif abs(piece) == 2:  # Cavalier
                    moves = cavalier(x, y, Bo, color_sign)
                    deplacements.extend([(x, y, nx, ny) for nx, ny in moves])
                elif abs(piece) == 5:  # Roi
                    moves = roi(x, y, Bo, color_sign)
                    deplacements.extend([(x, y, nx, ny) for nx, ny in moves])
                elif abs(piece) == 1:  # Tour
                    moves = tour(x, y, Bo, color_sign)
                    deplacements.extend([(x, y, nx, ny) for nx, ny in moves])
                elif abs(piece) == 3:  # Fou
                    moves = fou(x, y, Bo, color_sign)
                    deplacements.extend([(x, y, nx, ny) for nx, ny in moves])
                elif abs(piece) == 4:  # Reine
                    moves = reine(x, y, Bo, color_sign)
                    deplacements.extend([(x, y, nx, ny) for nx, ny in moves])
    return deplacements





# punition si répété
def penalize_repeated_moves(move, move_history):
    if move in move_history:
        return -0.5  # Pénalité pour un mouvement répété
    return 0


# Bot simple juste avec la valeur des pièces

def minimax(Bo, depth, alpha, beta, maximizing_player, color_sign, evaluate_board, start_time, time_limit):
    # Vérifier si le temps est écoulé
    if time.time() - start_time > time_limit:
        return evaluate_board(Bo, color_sign, [], [])

    # Condition de fin : profondeur atteinte ou partie terminée
    if depth == 0:
        return evaluate_board(Bo, color_sign, [], [])

    if maximizing_player:
        max_eval = -float('inf')
        for move in generer_deplacements(Bo, color_sign):
            new_board = appliquer_deplacement(Bo, move)
            eval = minimax(new_board, depth - 1, alpha, beta, False, color_sign, evaluate_board, start_time, time_limit)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Coupe bêta
        return max_eval
    else:
        min_eval = float('inf')
        for move in generer_deplacements(Bo, -color_sign):
            new_board = appliquer_deplacement(Bo, move)
            eval = minimax(new_board, depth - 1, alpha, beta, True, color_sign, evaluate_board, start_time, time_limit)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Coupe alpha
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

    MATE_SCORE = 100000  # Score très élevé pour le mat
    DRAW_SCORE = 0       # Score neutre pour les nulles
    CONTEMPT_FACTOR = 10 # Facteur de mépris pour éviter les nulles

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
    center_positions = [(3, 3), (3, 4), (4, 3), (4, 4)]
    for x, y in center_positions:
        piece = Bo[x][y]
        if piece * color_sign > 0:  # Pièce alliée au centre
            score += 50  # Bonus pour contrôler le centre
        elif piece * color_sign < 0:  # Pièce ennemie au centre
            score -= 50  # Malus si l'adversaire contrôle le centre

    # Mobilité
    moves = generer_deplacements(Bo, color_sign)
    mobility_score = len(moves) * 10  # Chaque coup disponible vaut 10 centipions
    score += mobility_score

    # Sécurité du roi
    if is_king_safe(Bo, color_sign):
        score += 100  # Bonus pour un roi en sécurité

    # Structure de pions
    for x in range(8):
        for y in range(8):
            piece = Bo[x][y]
            if abs(piece) == 6:  # Pion
                if piece * color_sign > 0:
                    # Bonus pour pions passés ou protégés
                    if is_pawn_passed(x, y, Bo, color_sign):
                        score += 50
                    if is_pawn_protected(x, y, Bo, color_sign):
                        score += 30
                    # Pénalité pour pions isolés ou doublés
                    if is_pawn_isolated(x, y, Bo):
                        score -= 30

    # Réduction des scores répétés
    if board_history:
        score += detect_repetition(Bo, board_history)

    return score

# fonction pour les eval
def is_king_in_check(Bo, color_sign):
    """
    Vérifie si le roi est en échec.
    :param Bo: Plateau actuel.
    :param color_sign: +1 pour les blancs, -1 pour les noirs.
    :return: True si le roi est en échec, False sinon.
    """
    king_position = None

    # Trouve la position du roi
    for x in range(8):
        for y in range(8):
            if Bo[x][y] == 5 * color_sign:  # Roi de la couleur donnée
                king_position = (x, y)
                break
    if not king_position:
        return False  # Aucun roi trouvé (cas improbable)

    x, y = king_position

    # Menaces des pions
    pawn_directions = [(-1, -1), (-1, 1)] if color_sign == 1 else [(1, -1), (1, 1)]
    for dx, dy in pawn_directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 8 and 0 <= ny < 8 and Bo[nx][ny] == -6 * color_sign:
            return True

    # Menaces des cavaliers
    knight_moves = [
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
    ]
    for dx, dy in knight_moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 8 and 0 <= ny < 8 and Bo[nx][ny] == -2 * color_sign:
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
            if Bo[nx][ny] == -3 * color_sign or Bo[nx][ny] == -4 * color_sign:
                return True
            if Bo[nx][ny] != 0:  # Collision avec une pièce
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
            if Bo[nx][ny] == -1 * color_sign or Bo[nx][ny] == -4 * color_sign:
                return True
            if Bo[nx][ny] != 0:  # Collision avec une pièce
                break

    # Menaces du roi adverse
    king_moves = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    for dx, dy in king_moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 8 and 0 <= ny < 8 and Bo[nx][ny] == -5 * color_sign:
            return True

    # Si aucune menace détectée
    return False

def is_checkmate(color_sign, Bo):
    """
    Vérifie si le joueur est en échec et mat.
    :param color_sign: +1 pour les blancs, -1 pour les noirs.
    :param Bo: Plateau.
    :return: True si le joueur est en échec et mat, False sinon.
    """
    moves = generer_deplacements(Bo, color_sign)
    if not moves and is_king_in_check(Bo, color_sign):
        return True
    return False

def is_king_safe(Bo, color_sign):
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

    return not is_king_in_check(Bo, color_sign)

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


#   Example how to register the function
register_chess_bot("simple", chess_bot_simple)
register_chess_bot("advanced", chess_bot_advanced)

