import random
from collections import deque

#
#   Example function to be implemented for
#       Single important function is next_best
#           color: a single character str indicating the color represented by this bot ('w' for white)
#           board: a 2d matrix containing strings as a descriptors of the board '' means empty location "XC" means a piece represented by X of the color C is present there
#           budget: time budget allowed for this turn, the function must return a pair (xs,ys) --> (xd,yd) to indicate a piece at xs, ys moving to xd, yd
#

from PyQt6 import QtCore

#   Be careful with modules to import from the root (don't forget the Bots.)
from Bots.ChessBotList import register_chess_bot

#   Simply move the pawns forward and tries to capture as soon as possible


def chess_bot_capture(player_sequence, board, time_budget, **kwargs):
    color = player_sequence[1]
    color_sign = 1 if color == 'w' else -1
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



    # Vérifie si une capture est possible
    capture_move = find_capture_move(B, color_sign)
    if capture_move:
        x1, y1, x2, y2 = capture_move
        return (x1, y1), (x2, y2)
    # Déplacement temporaire
    meilleur_deplacement = bfs_best_move(B, color_sign)
    x1, y1, x2, y2 = meilleur_deplacement
    return (x1, y1), (x2, y2)

def chess_bot_basic(player_sequence, board, time_budget, **kwargs):
    color = player_sequence[1]
    color_sign = 1 if color == 'w' else -1
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

    # Déplacement temporaire
    meilleur_deplacement = bfs_best_move(B, color_sign)
    x1, y1, x2, y2 = meilleur_deplacement
    return (x1, y1), (x2, y2)



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

def pos_pions(Bo, color_sign):
    positions = []
    for x in range(8):
        for y in range(8):
            if Bo[x][y] == 6 * color_sign:
                positions.append((x, y))
    return positions

def pos_cavaliers(Bo, color_sign):
    positions = []
    for x in range(8):
        for y in range(8):
            if Bo[x][y] == 2 * color_sign:
                positions.append((x, y))
    return positions

def pos_roi(Bo, color_sign):

    for x in range(8):
        for y in range(8):
            if Bo[x][y] == 5 * color_sign:  # Roi blanc = 5, roi noir = -5
                return x, y
    return None  # Si le roi n'est pas trouvé

def pos_tour(Bo, color_sign):
    """
    Trouve toutes les positions des tours alliées.
    """
    positions = []
    for x in range(8):
        for y in range(8):
            if Bo[x][y] == 1 * color_sign:  # Tour blanche = 1, tour noire = -1
                positions.append((x, y))
    return positions

def pos_fou(Bo, color_sign):
    """
    Trouve toutes les positions des fous alliés.
    """
    positions = []
    for x in range(8):
        for y in range(8):
            if Bo[x][y] == 3 * color_sign:  # Fou blanc = 3, fou noir = -3
                positions.append((x, y))
    return positions

def reine(pos_x, pos_y, Bo, color_sign):
    """
    Génère les déplacements possibles pour une reine.
    """
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),  # Directions de la tour
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # Directions du fou
    ]
    return get_moves_directions(Bo, pos_x, pos_y, color_sign, directions)

def pos_reine(Bo, color_sign):
    """
    Trouve toutes les positions des reines alliées.
    """
    positions = []
    for x in range(8):
        for y in range(8):
            if Bo[x][y] == 4 * color_sign:  # Reine blanche = 4, reine noire = -4
                positions.append((x, y))
    return positions

def get_moves_directions(Bo, pos_x, pos_y, color_sign, directions):
    """
    Génère les déplacements possibles dans les directions spécifiées.
    """
    moves = []
    for dx, dy in directions:
        nx, ny = pos_x + dx, pos_y + dy
        while 0 <= nx < 8 and 0 <= ny < 8:  # Vérifie que la position reste sur le plateau
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
    """
    Applique un déplacement au plateau et retourne une nouvelle copie du plateau.
    :param Bo: Plateau actuel
    :param move: Déplacement au format (x1, y1, x2, y2)
    :return: Nouveau plateau après le déplacement
    """
    x1, y1, x2, y2 = move
    new_board = [row[:] for row in Bo]  # Copie du plateau
    new_board[x2][y2] = new_board[x1][y1]  # Déplace la pièce
    new_board[x1][y1] = 0  # Vide la case d'origine
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

# Partie BFS

def score_board(board, color_sign):
    """
    Évalue le score d'un plateau en fonction des captures possibles.
    :param board: Plateau actuel
    :param color_sign: +1 pour les blancs, -1 pour les noirs
    :return: Score du plateau
    """
    score = 0
    piece_values = {
        1: 5,   # Tour
        2: 3,   # Cavalier
        3: 3,   # Fou
        4: 9,   # Reine
        5: 100, # Roi (priorité élevée mais non réaliste pour la capture ici)
        6: 10    # Pion
    }

    for x in range(8):
        for y in range(8):
            piece = board[x][y]
            if piece * color_sign < 0:  # Pièce ennemie
                # Vérifie si la pièce ennemie peut être capturée
                for move in generer_deplacements(board, color_sign):
                    x1, y1, x2, y2 = move
                    if x2 == x and y2 == y:  # Si un déplacement capture cette pièce
                        score += piece_values.get(abs(piece), 0)

    return score

def bfs_best_move(board, color_sign, depth=1):
    """
    Implémente un BFS simple pour trouver le meilleur déplacement possible.
    :param board: Plateau initial
    :param color_sign: +1 pour les blancs, -1 pour les noirs
    :param depth: Profondeur maximale de recherche
    :return: Meilleur déplacement sous la forme (x1, y1, x2, y2)
    """
    queue = deque([(board, None, 0)])  # (plateau, déplacement, profondeur)
    best_move = None
    best_score = float('-inf')
    first_level_moves = []

    while queue:
        current_board, last_move, current_depth = queue.popleft()

        if current_depth == 0:
            first_level_moves.append(last_move)

        if current_depth < depth:
            moves = generer_deplacements(current_board, color_sign)
            for move in moves:
                new_board = appliquer_deplacement(current_board, move)
                queue.append((new_board, move, current_depth + 1))

        else:
            # Évalue le score à la profondeur maximale
            score = score_board(current_board, color_sign)
            if score > best_score:
                best_score = score
                best_move = last_move

    # Si un meilleur mouvement a été trouvé, assurez-vous qu'il provient du premier niveau
    if best_move:
        for move in first_level_moves:
            if move and appliquer_deplacement(board, move) == appliquer_deplacement(board, best_move):
                return move

    return best_move

def find_capture_move(board, color_sign):

    for move in generer_deplacements(board, color_sign):
        x1, y1, x2, y2 = move
        if board[x2][y2] * color_sign < 0:  # Pièce ennemie sur la case de destination
            return move
    return None
#   Example how to register the function
register_chess_bot("capture", chess_bot_capture)
register_chess_bot("basique", chess_bot_basic)