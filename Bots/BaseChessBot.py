import random
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


def chess_bot(player_sequence, board, time_budget, **kwargs):
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


    #x1,y1,x2,y2 = meilleur_deplacement
    return (0,1),(2,2)



# trouver les déplacements possibles pour chaque pièce
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
    if 0 <= pos_x + direction <= 7 and Bo[pos_x + direction][pos_y] == 0:
        deplacements.append((pos_x + direction, pos_y))

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
def reine(pos_x, pos_y, Bo, color_sign):
    """
    Génère les déplacements possibles pour une reine.
    """
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),  # Directions de la tour
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # Directions du fou
    ]
    return get_moves_directions(Bo, pos_x, pos_y, color_sign, directions)
def fou(pos_x, pos_y, Bo, color_sign):
    """
    Génère les déplacements possibles pour un fou.
    """
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonales
    return get_moves_directions(Bo, pos_x, pos_y, color_sign, directions)

# trouver les positions des pièces
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


#heurisitcs
def heur_king_in_danger(board, color_sign):
    # board est le plateau après le déplacement effectué
    # color_sign est 1 pour les blancs et -1 pour les noirs
    opponent_sign = -color_sign

    # position du roi
    king_pos = pos_roi(board, color_sign)

    if not king_pos:
        return 0  #roi pas trouvé

    # checker si une pièce ennemie peut capturer le roi

    for x in range(8):
        for y in range(8):
            piece = board[x][y]
            if piece * color_sign < 0:  # Piece ennemie
                if  piece == opponent_sign * 1:
                    if king_pos in tour(x, y, board, opponent_sign):
                        return -500
                elif piece == opponent_sign * 2:
                    if king_pos in cavalier(x, y, board, opponent_sign):
                        return -500
                elif piece == opponent_sign * 3:
                    if king_pos in fou(x, y, board, opponent_sign):
                        return -500
                elif piece == opponent_sign * 4:
                    if king_pos in reine(x, y, board, opponent_sign):
                        return -500
                elif piece == opponent_sign * 6:
                    if king_pos in pion(x, y, board, opponent_sign):
                        return -500
                elif piece == opponent_sign * 5:
                    if king_pos in roi(x, y, board, opponent_sign):
                        return -500

    return 0  # Roi pas en danger

def heur_capture(board, color_sign, x, y, piece_id):
    score = 0
    piece_possible_movement = []
    match piece_id:
        case 1:
            piece_possible_movement = tour(x, y, board, color_sign)
        case 2:
            piece_possible_movement = cavalier(x, y, board, color_sign)
        case 3:
            piece_possible_movement = fou(x, y, board, color_sign)
        case 4:
            piece_possible_movement = reine(x, y, board, color_sign)
        case 5:
            piece_possible_movement = roi(x, y, board, color_sign)
        case 6:
            piece_possible_movement = pion(x, y, board, color_sign)

    for t in range(len(piece_possible_movement)):
        nx, ny = piece_possible_movement[t]
        if board[nx][ny] * color_sign < 0:  # si un ennemi est dans une des cases
            # TODO si chaque piece a un poids, donner + de score à celui qui a une différence de poids negative + grande (Ex: un pion qui mange la reine a + de score qu'une reine qui mange un pion)
            score += 200
            return score, (x,y,nx,ny)


    return score, (x, y, x, y)


#   Example how to register the function
register_chess_bot("PawnMover", chess_bot)