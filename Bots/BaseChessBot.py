
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
    print(board)
    for x in range(board.shape[0]-1):
        for y in range(board.shape[1]):
            '''
            ---Base code
            if board[x,y] != "p"+color:
                continue
            if y > 0 and board[x+1,y-1] != '' and board[x+1,y-1][-1] != color:
                return (x,y), (x+1,y-1)
            if y < board.shape[1] - 1 and board[x+1,y+1] != '' and board[x+1,y+1][1] != color:
                return (x,y), (x+1,y+1)
            elif board[x+1,y] == '':
                return (x,y), (x+1,y)
            '''

            '''
            ---Test Rook
            if board[x, y] != "r" + color:
                continue
            possible_moves = possible_moves_rook(board, x, y, color)
            if len(possible_moves) > 0:
                return (x,y), possible_moves[0]
            '''

            #---Test bishop
            if board[x, y] != "b" + color:
                continue
            possible_moves = possible_moves_bishop(board, x, y, color)
            if len(possible_moves) > 0:
                return (x,y), possible_moves[0]



    return (0,0), (0,0)


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