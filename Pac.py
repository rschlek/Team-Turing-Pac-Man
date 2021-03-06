import random
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
        self.chasing_super_pellet = False
        self.next_destination = None
        self.pac_chasing = None
        self.ability_meter_full = False
        self.rock = "ROCK"
        self.paper = "PAPER"
        self.scissors = "SCISSORS"
        self.command = ""
        self.prev_x
        self. prev_y

    '''
    controls the behavior of the Pac automatically provided Pac parameters are updated properly
    '''
    def play(self, board, enemy = None):  # to be called every turn by the gameplayloop in main, this way only one function call must be done on the object and all logic for each pac will run internally
        #self.command = ""
        stuck = self.is_stuck(board)
        self.prev_x = self.x
        self.prev_y = self.y
        if stuck:
            return
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
            if self.ability_meter_full:
                self.speed_boost()
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


    def is_stuck(self, board):
        if self.x == self.prev_x and self.y == self.prev_y:
            rand_unexplored = board.random_unexplored()
            if rand_unexplored is not None:
                next_x = rand_unexplored[1]
                next_y = rand_unexplored[0]
                self.move(next_x, next_y)
            return True
        return False

    '''
    called from the gameloop when an enemy is in sight.
    @:param enemy: a Pac object of the enemy Pac
    '''
    def see_enemy(self, enemy = None):
        if enemy is not None:
            self.attacking = True
            self.pac_chasing = enemy
        else:
            self.attacking = False
            self.pac_chasing = None


    def see_super_pellet(self, pellet_x = -1, pellet_y = -1):
        if (pellet_x < 0):
            self.chasing_super_pellet = False
            return
        self.chasing_super_pellet = True
        if self.x == pellet_x and self.y == pellet_y:
            self.chasing_super_pellet = False
        if self.next_destination != pellet_x + " " + pellet_y:
            self.next_destination = pellet_x + " " + pellet_y
            self.move(pellet_x, pellet_y)

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
