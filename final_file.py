import sys
import copy
import random
import math

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
        self.x = X
        self.y = Y
        self.friendly = friendly
        self.ability_cooldown = ability_cooldown
        self.speed_turns_left = speed_turns_left
        self.attacking = False
        self.chasing_super_pellet = False
        self.next_destination = None
        self.pac_chasing = None
        self.ability_meter_full = False
        self.rock = "ROCK"
        self.paper = "PAPER"
        self.scissors = "SCISSORS"
        self.command = ""

    '''
    controls the behavior of the Pac automatically provided Pac parameters are updated properly
    '''
    def play(self, board, enemy = None):  # to be called every turn by the gameplayloop in main, this way only one function call must be done on the object and all logic for each pac will run internally
        self.command = ''
        if self.ability_cooldown == 0:
            self.ability_meter_full = True
        elif self.ability_cooldown != 0:
            self.ability_meter_full = False

        
        if self.attacking: #make sure to set attacking to false and pac_chasing to None in the game loop if no enemy Pac is in sight #FIXME
            if self.pac_chasing is not None:
                self.attack_mode(self.pac_chasing.x, self.pac_chasing.y, self.pac_chasing.type_id)
            else: self.attacking = False
            return
        
        elif not self.attacking:
            if not self.chasing_super_pellet: #set to false if super pellet is reached or in game loop
                closest_pellet = board.closest_pellet(self.y, self.x)
                next_x = closest_pellet[1]
                next_y = closest_pellet[0]
                # for i in closest_pellet:
                #     if i is int:
                #         if next_x > -1:
                #             next_x = i
                #         elif next_y > -1:
                #             next_y = i
                self.move(next_x, next_y)
                return

        rand_unexplored = board.random_unexplored()
        if rand_unexplored is not None:
            next_x = rand_unexplored[1]
            next_y = rand_unexplored[0]
            self.move(next_x, next_y)
            return

        next_x = random.randint(0, board.width - 1)
        next_y = random.randint(0, board.height - 1)
        while board[next_x][next_y] == '#':
            next_x = random.randint(0, board.width - 1)
            next_y = random.randint(0, board.height - 1)
        self.move(next_x, next_y)

    '''
    prints the next move the Pac is going to take
    '''
    def next_move(self, next_move: str):
        self.command = next_move

    '''
    controls the Pac if an enemy is in sight
    '''
    def attack_mode(self, enemy_x = -1, enemy_y = -1, enemy_type = None):
        if enemy_x == -1:
            self.attacking = False
            self.pac_chasing = None
            return
        else:
            next_type = self.switch_to(self.type_id, enemy_type)
            if self.ability_meter_full:
                if next_type is not None:
                    self.switch(next_type)
                    #self.next_move("SWITCH " + self.id_num + " " + next_type)
                    return
                else:
                    self.speed_boost()
                    return

            next_location = enemy_x + " " + enemy_y
            if self.next_destination != next_location:
                self.next_destination = next_location
                #self.next_move("MOVE " + self.id_num + " " + next_destination)
                self.move(enemy_x, enemy_y)
                return

    '''
    determines the type that the Pac with 'my_type' should switch to given 'enemy_type'
    Note: this does not actually swith the pac, that is called from the 'switch' function
    '''
    def switch_to(self, my_type: str, enemy_type: str):
        if my_type == self.rock:
            if enemy_type == self.paper:
                return self.scissors
            elif enemy_type == self.rock:
                return self.paper
            elif enemy_type == self.scissors:
                return None
        elif my_type == self.scissors:
            if enemy_type == self.paper:
                return None
            elif enemy_type == self.rock:
                return self.paper
            elif enemy_type == self.scissors:
                return self.rock
        elif my_type == self.paper:
            if enemy_type == self.paper:
                return self.scissors
            elif enemy_type == self.rock:
                return None
            elif enemy_type == self.scissors:
                return self.rock


    # def gather_mode(self): #FIXME
    #     pass
    #
    # def update_ability_meter(self): #FIXME
    #     if self.ability_cooldown == 0:
    #         self.meter_full()
    #         self.ability_cooldown = 9
    #     else:
    #         self.ability_cooldown -= 1
    #
    # def meter_full(self): #FIXME
    #     if self.attacking:
    #         self.change_type()
    #     else:
    #         self.speed_boost()
    #
    # def get_location(self):  # -> Vector2: #FIXME
    #     return self.location
    #
    # def set_location(self, x, y): #FIXME
    #     self.location.x = x
    #     self.location.y = y


    def is_stuck(self) -> bool:
        return False

    '''
    called from the gameloop when an enemy is in sight.
    @:param enemy: a Pac object of the enemy Pac
    '''
    def see_enemy(self, board):
       # if board.board[][]
       #  self.pac_chasing = enemy
        x = self.x
        y = self.y

        while board.board[x][y] != '#':
            if board.board[x][y] == 'e':
                self.attacking = True
                self.pac_chasing = (x, y)
                return


    def see_super_pellet(self, pellet_x, pellet_y):
        self.chasing_super_pellet = True
        if self.x == pellet_x and self.y == pellet_y:
            self.chasing_super_pellet
        if self.next_destination != pellet_x + " " + pellet_y:
            self.next_destination = pellet_x + " " + pellet_y
            self.move(pellet_x, pellet_y)

    '''
    sets the next location the Pac will move to and calls the next_move function to print it
    '''
    def move(self, x: int, y: int):
        self.next_destination = str(x) + " " + str(y)
        self.next_move("MOVE " + str(self.id_num) + " " + str(x) + " " + str(y))

    '''
    sets the next type the Pac will switch to and calls the next_move function to print it
    '''
    def switch(self, switch_to: str):
        self.next_move("SWITCH " + str(self.type_id) + " " + switch_to)
        self.type_id = switch_to  # Remove this if type_id is being updated in the game loop FIXME

    '''
    calls next_move to print a speed boost call
    '''
    def speed_boost(self):
        self.next_move("SPEED " + str(self.id_num))







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


    

#temp

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
our_pacs = []
turn_command = ''
temp = 0

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

            our_pacs.append(pac)
            game.add_explored(x,y)
        if mine and not first:
            our_pacs[temp].x = x
            our_pacs[temp].y = y
            our_pacs[temp].speed_turns_left = speed_turns_left
            our_pacs[temp].ability_cooldown = ability_cooldown
            our_pacs[temp].type_id = type_id
            game.add_explored(x,y)
            temp += 1
        if not mine and not first:
            enemy = Pac(pac_id,type_id,x,y,True,ability_cooldown,speed_turns_left)

        game.update_board(' ',x,y)
        if (x,y) in game.pellet_locations:   
            err('Got Here deleting ', (x,y))
            game.pellet_locations.remove((x,y))


    temp = 0

    first = False

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

    for pac in our_pacs:
        pac.play(game)
        turn_command += pac.command + '|'

    print(turn_command)
    turn_command = ''
    