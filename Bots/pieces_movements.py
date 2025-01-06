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
def apply_move(Bo, move):
    x1, y1, x2, y2 = move
    new_board = [row[:] for row in Bo]  # Copie profonde du plateau
    new_board[x2][y2] = new_board[x1][y1]
    new_board[x1][y1] = 0
    return new_board


def generate_moves(board, color_sign):
    """
    Generate all possible moves for a given player.
    Prioritizes capturing the opponent's king.
    """
    moves = []
    king_capture_moves = []

    for x in range(8):
        for y in range(8):
            piece = board[x][y]
            if piece * color_sign > 0:  # Player's pieces
                if abs(piece) == 6:  # Pawn
                    possible_moves = pion(x, y, board, color_sign)
                elif abs(piece) == 2:  # Knight
                    possible_moves = cavalier(x, y, board, color_sign)
                elif abs(piece) == 5:  # King
                    possible_moves = roi(x, y, board, color_sign)
                elif abs(piece) == 1:  # Rook
                    possible_moves = tour(x, y, board, color_sign)
                elif abs(piece) == 3:  # Bishop
                    possible_moves = fou(x, y, board, color_sign)
                elif abs(piece) == 4:  # Queen
                    possible_moves = reine(x, y, board, color_sign)
                else:
                    possible_moves = []

                for nx, ny in possible_moves:
                    if abs(board[nx][ny]) == 5 * -color_sign:  # Opponent's king
                        king_capture_moves.append((x, y, nx, ny))
                    else:
                        moves.append((x, y, nx, ny))

    if king_capture_moves:
        return king_capture_moves  # Always prioritize king capture

    return moves
