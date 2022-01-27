import sys
import copy

def err(*args):
    sys.stderr.write(', '.join([str(arg) for arg in args]) + "\n")


'''
Class to track the board/state of the game
'''
class state:
    def __init__(self, rows, width, height, board=None):
        if board is not None:
            self.board=board
            self.height = len(board)
            self.width = len(board[0])
        else:
        
            self.board = []
            self.height = height
            self.width = width

            for i in range(height):
                self.board.append([])
                for j in range(width):
                    self.board[i].append(rows[i][j])

        self.available_coords = []

        for i in range(height):
            for j in range(width):
                if self.board[height][width] != '#':
                    self.available_coords.append((height,width))

        '''
        Stores the locations of known pellets
        '''
        self.pellet_locations = []
        self.explored_squares = []

    '''
    Updates the board at a certain coordinate with a symbol
    wall = '#'
    space = ' '
    pellet = 'o'
    super pellet = 'O'
    enemy pac = 'e'
    friendly pac = 'f'
    '''
    def update_board(self,symbol,width,height):
        if self.board[height][width] == '#':
            err('Invalid coordinate')
        else:
            self.board[height][width] = symbol

    '''
    Returns a copy of the board that won't change the original instance of the class
    '''
    def copy_board(self):
        return copy.deepcopy(self.board)

    '''
    Returns the closest pellet available to a coordinate (last seen by a friendly pac)
    (height,width)
    '''
    def closest_pellet(self, height, width):
        closest_distance = 10000
        closest_coord = (-1,-1)
        for i in range(len(self.pellet_locations)):
            distance = abs(height-self.pellet_locations[i][0]) + abs(width-self.pellet_locations[i][1])
            if distance < closest_distance:
                closest_distance = distance
                closest_coord = self.pellet_locations[i]
        
        return closest_coord

# width: size of the grid
# height: top left corner is (x=0, y=0)
width, height = [int(i) for i in input().split()]
rows = []
for i in range(height):
    row = input()
    rows.append(row)    # one line of the grid: space " " is floor, pound "#" is wall

game = state(rows,width,height)

# game loop
while True:
    my_score, opponent_score = [int(i) for i in input().split()]
    visible_pac_count = int(input())  # all your pacs and enemy pacs in sight
    for i in range(visible_pac_count):
        inputs = input().split()
        pac_id = int(inputs[0])  # pac number (unique within a team)
        mine = inputs[1] != "0"  # true if this pac is yours
        x = int(inputs[2])  # position in the grid
        y = int(inputs[3])  # position in the grid
        type_id = inputs[4]  # unused in wood leagues
        speed_turns_left = int(inputs[5])  # unused in wood leagues
        ability_cooldown = int(inputs[6])  # unused in wood leagues
    visible_pellet_count = int(input())  # all pellets in sight
    for i in range(visible_pellet_count):
        # value: amount of points this pellet is worth
        x, y, value = [int(j) for j in input().split()]
        if value > 1:
            game.update_board('O',)


    # Everything above this are inputs from the game


