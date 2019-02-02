
import random
import math
import copy

class Domineering():
    def __init__(self, turn='v', move=None, board=None):
        self.turn = turn
        self.move = move
        self.board = board if board != None else [['-' for _ in range(8)] for _ in range(8)]
        
    def children(self):
        children = []
        if self.turn == 'v':
            for row in range(len(self.board)-1):
                for col in range(len(self.board)):
                    if self.board[row][col] == '-' and self.board[row+1][col] == '-':
                        child_board = copy.deepcopy(self.board)
                        child_board[row][col], child_board[row+1][col] = 'v', 'v'
                        children.append(Domineering(turn='h', board=child_board, move=(row, col)))

        elif self.turn == 'h':
            for row in range(len(self.board)):
                for col in range(len(self.board)-1):
                    if self.board[row][col] == '-' and self.board[row][col+1] == '-':
                        child_board = copy.deepcopy(self.board)
                        child_board[row][col], child_board[row][col+1] = 'h', 'h'
                        children.append(Domineering(turn='v', board=child_board, move=(row, col)))
        return children
    
    def heuristic(self):
        options_v, options_h = 0, 0
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if self.board[row][col]=='-' and row+1<len(self.board) and self.board[row+1][col]=='-':
                    options_v += 1
                if self.board[row][col]=='-' and col+1<len(self.board) and self.board[row][col+1]=='-':
                    options_h += 1
        return (options_v - options_h) if self.turn == 'v' else (options_h - options_v)


def alpha_beta(node, depth=2, a=-math.inf, b=math.inf, maximizing_player=True):
    if depth == 0:
        return [node.heuristic(), None]
    if maximizing_player:
        value = [-math.inf, None]
        for child in node.children():
            recurse_res = alpha_beta(child, depth-1, a, b, False)
            if recurse_res[0] > value[0]:
                value[0] = recurse_res[0]
                value[1] = child.move
            a = max(a, value[0])
            if a >= b: break
        return value
    else:
        value = [math.inf, None]
        for child in node.children():
            recurse_res = alpha_beta(child, depth-1, a, b, True)
            if recurse_res[0] < value[0]:
                value[0] = recurse_res[0]
                value[1] = child.move
            b = min(b, value[0])
            if a >= b: break
        return value

# gather inputs
player = input()
board = [list(input()) for _ in range(8)]

move = alpha_beta(Domineering(turn=player, board=board))[1]
print(move[0], move[1])
