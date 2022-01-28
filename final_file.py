import sys
import copy
import random

def err(*args):
    sys.stderr.write(', '.join([str(arg) for arg in args]) + "\n")




class Pac:

    #    id_num
    #   type_id
    #    location = Vector2(0, 0) # a vector 2 containing an x and y value to denote position
    #   enemy # a boolean denoting if the pac is an enemy or not, true if enemy. If true, only the location and type_id fields are relevant
    #  attack_mode = False
    # next_destination
    # ability_cooldown # an int representing the level of the ability meter. 10 = full, 0 = usable
    #        speed_turns_left # an int denoting the number of turns left for the speed boost
    #       meter_full = true
    #      pac_chasing # the enemy Pac that is/was-recently in view that is being chased by this pac
    #     enemy_in_view = false

    def __init__(self, id_num, type_id, X: int, Y: int, friendly: bool, ability_cooldown: int, speed_turns_left: int):
        self.id_num = id_num
        self.type_id = type_id
        self.location = (X,Y)
        self.friendly = friendly
        self.ability_cooldown = ability_cooldown
        self.speed_turns_left = speed_turns_left
        self.attacking = False
       # self.next_destination = next_destination

    def play(self, enemy = None):  # to be called every turn by the gameplayloop in main, this way only one function call must be done on the object and all logic for each pac will run internally
        self.update_ability_meter()

        if self.attacking:
            self.attack_mode(enemy)
        else:
            self.gather_mode()

    def attack_mode(self, enemy):
        if self.pac_chasing is not None:
            next_location = self.id_num + " " + self.pac_chasing.position.x + " " + self.pac_chasing.position.y
            if self.next_destination != next_location:
                next_destination = next_location
                print(next_destination)

    def gather_mode(self):
        pass

    def update_ability_meter(self):
        if self.ability_cooldown == 0:
            self.meter_full()
            self.ability_cooldown = 10
        else:
            self.ability_cooldown -= 1

    def meter_full(self):
        if self.attacking:
            self.change_type()
        else:
            self.speed_boost()

    def change_type(self):
        pass

    def speed_boost(self):
        print(self.id_num + " SPEED")

    def get_location(self):  # -> Vector2:
        return self.location

    def set_location(self, x, y):
        self.location = (x,y)
        

    def is_stuck(self) -> bool:
        return False

    def see_enemy(self, enemy):
        self.pac_chasing = enemy
        self.attacking = True

    def check_best_path(self, position, board = None):
        if board is not None:
            x = position.x
            y = position.y
            up_pellets, down_pellets, left_pellets, right_pellets = 0, 0, 0, 0
            up = ""
            down = ""
            left = ""
            right = ""

            index = board[position.x][position.y]
            while index != '#':
                y -= 1
                index = board[x][y]
                if index != '#':
                    up += index + " "

            index = board[position.x][position.y]
            x = position.x
            y = position.y
            while index != '#':
                y += 1
                index = board[x][y]
                if index != '#':
                    down += index + " "

            index = board[position.x][position.y]
            x = position.x
            y = position.y
            while index != '#':
                x -= 1
                index = board[x][y]
                if index != '#':
                    left += index + " "

            index = board[position.x][position.y]
            x = position.x
            y = position.y
            while index != '#':
                x += 1
                index = board[x][y]
                if index != '#':
                    right += index + " "

            for i in up:
                if i == 'o':
                    up_pellets += 1
                elif i == 'O':
                    up_pellets += 10
                elif i == 'e':
                    return "UP"

            for i in down:
                if i == 'o':
                    down_pellets += 1
                elif i == 'O':
                    down_pellets += 10
                elif i == 'e':
                    return "DOWN"

            for i in left:
                if i == 'o':
                    left_pellets += 1
                elif i == 'O':
                    left_pellets += 10
                elif i == 'e':
                    return "LEFT"

            for i in right:
                if i == 'o':
                    right_pellets += 1
                elif i == 'O':
                    right_pellets += 10
                elif i == 'e':
                    return "RIGHT"

            if up_pellets >= down_pellets and up_pellets >= left_pellets and up_pellets >= right_pellets:
                return "UP"

            if down_pellets >= up_pellets and down_pellets >= left_pellets and down_pellets >= right_pellets:
                return "DOWN"

            if left_pellets >= up_pellets and left_pellets >= down_pellets and left_pellets >= right_pellets:
                return "LEFT"

            if right_pellets >= up_pellets and right_pellets >= down_pellets and right_pellets >= left_pellets:
                return "RIGHT"


class Vector2:

    def __init__(self, x, y):
        self.x = x
        self.y = y







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
                    self.available_coords.append((j,i))

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
            self.pellet_locations.append((height,width))


    



# Below this line is the game loop information




# width: size of the grid
# height: top left corner is (x=0, y=0)
width, height = [int(i) for i in input().split()]
rows = []
for i in range(height):
    row = input()
    rows.append(row)    # one line of the grid: space " " is floor, pound "#" is wall

game = state(rows,width,height)

first = True
our_pacs = {}
turn_command = ''

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

        if first and mine:
            name = pac_id
            pac = Pac(pac_id,type_id,x,y,True,ability_cooldown,speed_turns_left)

            our_pacs[i] = pac
            game.add_explored(x,y)
        if mine and not first:
            our_pacs[pac_id].x = x
            our_pacs[pac_id].y = y
            our_pacs[pac_id].speed_turns_left = speed_turns_left
            our_pacs[pac_id].ability_cooldown = ability_cooldown



    visible_pellet_count = int(input())  # all pellets in sight
    for i in range(visible_pellet_count):
        # value: amount of points this pellet is worth
        x, y, value = [int(j) for j in input().split()]
        
        # Added to update board of values of pellets
        if value > 1:
            game.update_board('O',x,y)
            game.add_pellet(x,y)
        else:
            game.update_board('o',x,y)
            game.add_pellet(x,y)

    err(game.available_coords,game.random_unexplored())