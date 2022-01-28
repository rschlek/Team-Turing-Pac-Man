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
                if self.board[i][j] != '#':
                    self.available_coords.append((i,j))

        '''
        Stores the locations of known pellets
        '''
        self.pellet_locations = []
        self.explored_squares = []

        self.visited = []

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
            err('Invalid coordinate (update_board)')
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

    def add_explored(self,width,height):
        if (width,height) not in self.explored_squares:
            self.explored_squares.append((width,height))
        wall = False
        if width < self.width-1:
            for i in range(width+1, self.width):
                if self.board[height][i] == '#':
                    wall = True
                if not wall:
                    self.explored_squares.append((i,height))
            wall = False
        if width > 0:
            for i in reversed(range(0,width)):
                if self.board[height][i] == '#':
                    wall = True
                if not wall:
                    self.explored_squares.append((i,height))
            wall = False
        if height > 0:
            for i in reversed(range(0,height)):
                if self.board[i][width] == '#':
                    wall = True
                if not wall:
                    self.explored_squares.append((width,i))
            wall=False
        if height<self.height-1:
            for i in range(height+1,self.height):
                if self.board[i][width] =='#':
                    wall = True
                if not wall:
                    self.explored_squares.append((width,i))
            wall=False
                
        


    def random_unexplored(self):
        unexplored_coords = copy.deepcopy(self.available_coords)
        for element in unexplored_coords:
            if element in self.explored_squares:
                unexplored_coords.remove(element)

        return random.choice(unexplored_coords)



    def add_pellet(self, width, height):
        if self.board[height][width] == '#':
            err('Invalid coordinate (add_pellet)')
        else:
            self.pellet_locations.append((width,height))
