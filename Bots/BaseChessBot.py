
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
        direction = -1 if color_sign == 1 else 1

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

    # Trouver les pions et les cavaliers
    pions = pos_pions(B, color_sign)
    cavaliers = pos_cavaliers(B, color_sign)

    # Choisir aléatoirement entre les pions et les cavaliers
    '''
    if not pions and not cavaliers:
        return None  # Aucun mouvement possible
    elif not pions:
        piece_type = "cavalier"
    elif not cavaliers:
        piece_type = "pion"
    else:
        piece_type = random.choice(["pion", "cavalier"])

    if piece_type == "pion":
        pion_pos = random.choice(pions)
        deplacements = pion(pion_pos[0], pion_pos[1], B, color_sign)
        if deplacements:
            choix_deplacement = random.choice(deplacements)
            return pion_pos, choix_deplacement
    elif piece_type == "cavalier":
        cavalier_pos = random.choice(cavaliers)
        deplacements = cavalier(cavalier_pos[0], cavalier_pos[1], B, color_sign)
        if deplacements:
            choix_deplacement = random.choice(deplacements)
            return cavalier_pos, choix_deplacement
    '''
    piece_type = "cavalier"
    cavalier_pos = random.choice(cavaliers)
    deplacements = cavalier(cavalier_pos[0], cavalier_pos[1], B, color_sign)
    choix_deplacement = random.choice(deplacements)
    return cavalier_pos, choix_deplacement







def possible_moves_rook(board, x, y, color):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return get_moves_directions(board, x, y, color, directions)

def possible_moves_bishop(board, x, y, color):
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    return get_moves_directions(board, x, y, color, directions)

def possible_moves_queen(board, x, y, color):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    return get_moves_directions(board, x, y, color, directions)

def get_moves_directions(board, x, y, color, directions):
    moves = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        while 0 <= nx < 8 and 0 <= ny < 8:
            target = board[nx][ny]
            if target == '':
                moves.append((nx, ny))
            elif target[1] != color:
                # TODO: Check si ca vaut la peine de capturer
                moves.append((nx, ny))
                break
            else:
                break  # piece de meme couleur

            nx, ny = nx + dx, ny + dy

    return moves


#   Example how to register the function
register_chess_bot("PawnMover", chess_bot)