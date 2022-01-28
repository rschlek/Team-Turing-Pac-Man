import sys
import math


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
        self.see_super_pellet = False
        self.next_destination = None
        self.ability_meter_full = False
        self.rock = "ROCK"
        self.paper = "PAPER"
        self.scissors = "SCISSORS"

    '''
    controls the behavior of the Pac automatically provided Pac parameters are updated properly
    '''
    def play(self, enemy = None):  # to be called every turn by the gameplayloop in main, this way only one function call must be done on the object and all logic for each pac will run internally
        if self.ability_cooldown == 0:
            self.ability_meter_full = True
        elif self.ability_cooldown != 0:
            self.ability_meter_full = False

        if self.attacking:
            pass

        elif not self.attacking:
            pass

    '''
    prints the next move the Pac is going to take
    '''
    def next_move(self, next_move: str):
        print(next_move)

    '''
    controls the Pac if an enemy is in sight
    '''
    def attack_mode(self, enemy_x = -1, enemy_y = -1, enemy_type = None):
        if enemy_x == -1:
            self.attacking = False
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

            next_location = self.id_num + " " + enemy_x + " " + enemy_y
            if self.next_destination != next_location:
                next_destination = next_location
                #self.next_move("MOVE " + self.id_num + " " + next_destination)
                self.move(enemy_x, enemy_y)
                return

    '''
    determines the type that the Pac with 'my_type' should switch to given 'enemy_type'
    Note: this does not actually swith the pac, that is called from the 'switch' function
    '''
    def switch_to(self, my_type: str, enemy_type: str) -> str:
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


    def gather_mode(self):
        pass

    def update_ability_meter(self): #FIXME
        if self.ability_cooldown == 0:
            self.meter_full()
            self.ability_cooldown = 9
        else:
            self.ability_cooldown -= 1

    def meter_full(self): #FIXME
        if self.attacking:
            self.change_type()
        else:
            self.speed_boost()

    def get_location(self):  # -> Vector2: #FIXME
        return self.location

    def set_location(self, x, y): #FIXME
        self.location.x = x
        self.location.y = y

    def is_stuck(self) -> bool:
        return False

    '''
    called from the gameloop when an enemy is in sight.
    @:param enemy: a Pac object of the enemy Pac
    '''
    def see_enemy(self, enemy):
        self.pac_chasing = enemy
        self.attacking = True
    '''
    sets the next location the Pac will move to and calls the next_move function to print it
    '''
    def move(self, x: int, y: int):
        self.next_destination = x + " " + y
        self.next_move("MOVE " + self.id_num + " " + x + " " + y)

    '''
    sets the next type the Pac will switch to and calls the next_move function to print it
    '''
    def switch(self, switch_to: str):
        self.next_move("SWITCH " + self.type_id + " " + switch_to)
        self.type_id = switch_to  # Remove this if type_id is being updated in the game loop FIXME

    '''
    calls next_move to print a speed boost call
    '''
    def speed_boost(self):
        self.next_move("SPEED " + self.id_num)

    def check_best_path(self, position, board = None): #FIXME
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


