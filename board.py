import sys
import copy

class state:
    def __init__(self, rows, width, height, board=None):
        if board is not None:
            self.board=board
        else:
        
            self.board = []
            self.height = height
            self.width = width

            for i in range(height):
                self.board.append([])
                for j in range(width):
                    self.board[i].append(rows[i][j])

    def update_board(self,symbol,height,width):
        self.board[height][width] = symbol

    def copy_board(self):
        return copy.deepcopy(self.board)