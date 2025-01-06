
# possible moves for each piece

def knight(pos_x, pos_y, board, color_sign):
    movements = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]
    moves = []
    for dx, dy in movements:
        nx, ny = pos_x + dx, pos_y + dy
        if 0 <= nx <= 7 and 0 <= ny <= 7:
            piece = board[nx][ny]
            if piece == 0 or (piece * color_sign < 0):  # empty or enemy piece
                moves.append((nx, ny))
    return moves

def pawn(pos_x, pos_y, board, color_sign):
    moves = []
    direction = 1

    # forward
    nx = pos_x + direction
    if 0 <= nx <= 7 and board[nx][pos_y] == 0:  # empty square
        moves.append((nx, pos_y))

    # diagonal
    for dy in [-1, 1]:
        nx, ny = pos_x + direction, pos_y + dy
        if 0 <= nx <= 7 and 0 <= ny <= 7:
            if board[nx][ny] * color_sign < 0:  # enemy piece
                moves.append((nx, ny))

    return moves

def king(pos_x, pos_y, board, color_sign):
    mouvements = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    moves = []

    for dx, dy in mouvements:
        nx, ny = pos_x + dx, pos_y + dy
        if 0 <= nx <= 7 and 0 <= ny <= 7:  # check boundaries
            piece = board[nx][ny]
            if piece == 0 or piece * color_sign < 0: # empty or enemy piece
                moves.append((nx, ny))

    return moves

def rook(pos_x, pos_y, board, color_sign):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return get_moves_directions(board, pos_x, pos_y, color_sign, directions)

def bishop(pos_x, pos_y, board, color_sign):
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    return get_moves_directions(board, pos_x, pos_y, color_sign, directions)

def queen(pos_x, pos_y, board, color_sign):
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (-1, 1), (1, -1), (1, 1)
    ]
    return get_moves_directions(board, pos_x, pos_y, color_sign, directions)

# function to get moves in a specific direction
def get_moves_directions(board, pos_x, pos_y, color_sign, directions):

    moves = []
    for dx, dy in directions:
        nx, ny = pos_x + dx, pos_y + dy
        while 0 <= nx < 8 and 0 <= ny < 8:
            piece = board[nx][ny]
            if piece == 0:
                moves.append((nx, ny))
            elif piece * color_sign < 0:  # enemy piece
                moves.append((nx, ny))
                break
            else:  # ally piece
                break
            nx += dx
            ny += dy
    return moves

# apply move to the board, used for evaluation
def apply_move(board, move):
    x1, y1, x2, y2 = move
    new_board = [row[:] for row in board]  # Copie profonde du plateau
    new_board[x2][y2] = new_board[x1][y1]
    new_board[x1][y1] = 0
    return new_board

# generate all possible moves for a player
def generate_moves(board, color_sign):
    moves = []
    #priority to capture the king
    king_capture_moves = []

    for x in range(8):
        for y in range(8):
            piece = board[x][y]
            if piece * color_sign > 0:  # Player's pieces
                if abs(piece) == 6:  # Pawn
                    possible_moves = pawn(x, y, board, color_sign)
                elif abs(piece) == 2:  # Knight
                    possible_moves = knight(x, y, board, color_sign)
                elif abs(piece) == 5:  # King
                    possible_moves = king(x, y, board, color_sign)
                elif abs(piece) == 1:  # Rook
                    possible_moves = rook(x, y, board, color_sign)
                elif abs(piece) == 3:  # Bishop
                    possible_moves = bishop(x, y, board, color_sign)
                elif abs(piece) == 4:  # Queen
                    possible_moves = queen(x, y, board, color_sign)
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
