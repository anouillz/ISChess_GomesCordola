
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
            possible_moves = possible_moves_rook(x,y)
            if board[possible_moves[0]] == '':
                return (x,y), possible_moves[0]
            '''
            '''
            ---Test bishop
            if board[x, y] != "b" + color:
                continue
            possible_moves = possible_moves_bishop(x,y)
            if board[possible_moves[0]] == '':
                return (x,y), possible_moves[0]
            '''


    return (0,0), (0,0)


def possible_moves_rook(x, y):
    moves = []
    for i in range(1, 8):
        if x + i < 8:
            moves.append((x + i, y))
        if x - i >= 0:
            moves.append((x - i, y))
        if y + i < 8:
            moves.append((x, y + i))
        if y - i >= 0:
            moves.append((x, y - i))
    print(moves)
    return moves

def possible_moves_bishop(x,y):
    moves = []
    for i in range(1,8):
        if x+i < 8 and y+i < 8:
            moves.append((x+i, y+i))
        if x+i < 8 and y-i > 0:
            moves.append((x+i, y-i))
        if x-i > 0 and y+i < 8:
            moves.append((x-i, y+i))
        if x-i > 0 and y-i > 0:
            moves.append((x-i, y-i))
    return moves

def possible_moves_queen(x, y):
    moves = []
    for i in range(1, 8):
        if x+i < 8:
            moves.append((x+i, y))
        if x-i >= 0:
            moves.append((x-i, y))
        if y+i < 8:
            moves.append((x, y+i))
        if y-i >= 0:
            moves.append((x, y-i))
        if x+i < 8 and y+i < 8:
            moves.append((x+i, y+i))
        if x+i < 8 and y-i >= 0:
            moves.append((x+i, y-i))
        if x-i >= 0 and y+i < 8:
            moves.append((x-i, y+i))
        if x-i >= 0 and y-i >= 0:
            moves.append((x-i, y-i))
    return moves

def canMove_r(x,y, board, player_sequence):
    color = player_sequence[1]
    isValid = True
    if (board[x, y+1] or board[x, y-1] or board[x+1, y] or board[x-1, y]) != '':
        isValid = False
    return isValid


#   Example how to register the function
register_chess_bot("PawnMover", chess_bot)