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
        self.location.x = x
        self.location.y = y

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

