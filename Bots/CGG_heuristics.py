
from Bots.CGG_chess_piece_moves import apply_move, generate_moves
#heuristics

#heuristic for king protection -------

def get_king_position(board, color_sign):
    king_position = None
    for x in range(8):
        for y in range(8):
            if board[x][y] == 5 * color_sign:  #king of given color
                king_position = (x, y)
                break
    if not king_position:
        return False  # no king found, impossible
    return king_position

#checks if the king is in threat by any opponent piece
def heuristic_king_inThreat(board, color_sign):
    x,y = get_king_position(board, color_sign)

    # pawn threats
    pawn_directions = [(-1, -1), (-1, 1)] if color_sign == 1 else [(1, -1), (1, 1)]
    for dx, dy in pawn_directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 8 and 0 <= ny < 8 and board[nx][ny] == -6 * color_sign:
            return True

    # knight threats
    knight_moves = [
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
    ]
    for dx, dy in knight_moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 8 and 0 <= ny < 8 and board[nx][ny] == -2 * color_sign:
            return True


    # bishop and queen threats
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

    # rook and queen threats
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

    # opposite king threats
    king_moves = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    for dx, dy in king_moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 8 and 0 <= ny < 8 and board[nx][ny] == -5 * color_sign:
            return True

    # if not threatened
    return False

#checks if the king of the color sign is in checkmate
def is_checkmate(color_sign, board):
    moves = generate_moves(board, color_sign)
    if not moves and heuristic_king_inThreat(board, color_sign):
        return True
    return False

# checks if king in safe position
def heuristic_king_safe(board, color_sign):
    king_position = None
    for x in range(8):
        for y in range(8):
            if board[x][y] == 5 * color_sign:  # get king position
                king_position = (x, y)
                break
    if not king_position:
        return False  # case not possible

    return not heuristic_king_inThreat(board, color_sign)


#heuristic for pawn aligned ----------

# checks if a pawn is passed, isolated, or protected
def is_pawn_passed(x, y, board, color_sign):
    direction = 1 if color_sign == 1 else -1
    for nx in range(x + direction, 8 if color_sign == 1 else -1, direction):
        for dy in [-1, 0, 1]:
            ny = y + dy
            if 0 <= ny < 8 and board[nx][ny] * color_sign < 0 and abs(board[nx][ny]) == 6:
                return False  # opposing pawn in the way
    return True

def is_pawn_protected(x, y, board, color_sign):
    for dx, dy in [(1, -1), (1, 1)] if color_sign == 1 else [(-1, -1), (-1, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 8 and 0 <= ny < 8 and board[nx][ny] == 6 * color_sign:
            return True # Protected by another pawn
    return False

def is_pawn_isolated(x, y, Bo):
    for dx, dy in [(1, -1), (1, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 8 and 0 <= ny < 8 and Bo[nx][ny] == 6:
            return False  # allied pawn nearby
    return True

def heuristic_pawn_aligned(board, color_sign):
    for x in range(8):
        for y in range(8):
            piece = board[x][y]
            if abs(piece) == 6:  # Pion
                if piece * color_sign > 0:
                    # bonus for passed or protected pawns
                    if is_pawn_passed(x, y, board, color_sign):
                        return 50
                    if is_pawn_protected(x, y, board, color_sign):
                        return 30
                    # penalty for isolated pawns
                    if is_pawn_isolated(x, y, board):
                        return -30
    return 0


#heuristic for board center control ------
#get total nb of pieces in the board
def get_nb_pieces(board):
    count = 0
    for x in range(len(board)):
        for y in range(len(board)):
            if board[x][y] != 0:
                count += 1
    return count
def heuristic_board_center(board, color_sign):

    center_positions = [(2,2),(2,3),(2,4),(2,5),(3,2),(3,5),(4,2),(4,5),(5,2),(5,3),(5,4),(5,5)]

    # not useful after 25 pieces
    if get_nb_pieces(board) > 25:
        for x, y in center_positions:
            piece = board[x][y]
            if piece * color_sign > 0:  # ally in the center
                return 50
            elif piece * color_sign < 0:  # enemy in the center
                return -50

    return 0


#checks if a move has been repeated -------
def detect_repetition(board, board_history):

    count = board_history.count(board)
    if count > 2:
        return -20
    return 0

#capture heuristic ------
def capture_heuristic(board, color_sign, piece_values):

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

