import sys
import math
import random

def distf(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def vision(x,y,area):
    opts = [[x,y]]
    up = True
    down = True
    left = True
    right = True
    for i in range(10):
        if right and x + i < len(area[0]):  
            if area[y][x+i] not in ["#", "R", "P", "S", "T"]:
                opts.append([x+i, y])
            else:
                right = False
        if left and x - i >= 0:
            if area[y][x-i] not in ["#", "R", "P", "S", "T"]:
                opts.append([x-i,y])
            else:
                left = False
        if up and y - i >= 0:
            if area[y-i][x] not in ["#", "R", "P", "S", "T"]:
                opts.append([x,y-i])
            else:
                up = False
        if down and y + i < len(area):
            if area[y+i][x] not in ["#", "R", "P", "S", "T"]:
                opts.append([x,y+i])
            else:
                down = False
    return opts
    
def counter(x):
    if x == "R":
        return "P"
    elif x == "P":
        return "S"
    else:
        return "R"

def moves(x,y,area):
    up = [x,y-1]
    down = [x,y+1]
    left = [x-1,y]
    right = [x+1,y]
    moves = []
    
    for move in [up,down,left,right]:
        if y not in range(0, height-1):
            break
        if move[0] >= width and area[y][0] not in ["#"]:
            moves.append([0, y])
        elif move[0] < 0 and area[y][width-1] not in ["#"]:
            moves.append([width-1,y])
        elif move[0] in range(0,width):
            moves.append(move)
    return moves

def good_runs(x,y,area, data_enemies, enemy_places, n=4):
    sol_ids = []
    sols = []
    moves1 = moves(x,y,area)

    for a in range(n):
        moves2 = []
        moves3 = []
        for m in moves1:
            if m not in sol_ids:
                sol_ids.append(m)
                if repr([m[0],m[1],area,enemy_places]) in danger_cache:
                    sols.append([1/(danger_cache[repr([m[0],m[1],area,enemy_places])][0]), m])
                else:
                    store = danger(m[0],m[1],area,enemy_places)
                    sols.append([1/store[0], m])
                    danger_cache[repr([m[0],m[1],area,enemy_places])] = store
            if area[m[1]][m[0]] in ["1", " ", ".", "9"]:
                if m not in moves2:
                    moves2.append(m)
        for i in moves2:
            j = moves(i[0],i[1],area)  
            for k in j:
                if k not in moves3:
                    moves3.append(k)
        moves1 = moves3
    if len(sols) == 0:
        return [x,y]
    else:
        sols = sorted(sols)
        return sols[0][1]

def danger(x,y,area, enemy_places, n=5):
    moves1 = moves(x,y,area)
    sols = []
    sol_ids = []
    for a in range(n):
        moves2 = []
        moves3 = []
        for m in moves1:
            if m not in sol_ids:
                #print(m,file=sys.stderr)
                if enemy_places[m[1]][m[0]] != "O":
                    sols.append([1/(0.1+distf([x,y],m)), area[m[1]][m[0]]])
                sol_ids.append(m)
            if area[m[1]][m[0]] in ["1", " ", ".", "9"]:
                if m not in moves2:
                    moves2.append(m)
        for i in moves2:
            j = moves(i[0],i[1],area)  
            for k in j:
                if k not in moves3:
                    moves3.append(k)
        moves1 = moves3
    if len(sols) == 0:
        return [9001, None]
    else:
        sols = sorted(sols)
        return (sum([i[0] for i in sols]), sols[0][1])

def good_moves(x,y,area, n=15):
    sols = []
    moves1 = moves(x,y,area)
    for a in range(n):
        moves2 = []
        moves3 = []
        for m in moves1:
            if area[m[1]][m[0]] in ["1","9"]:
                if m not in sols:
                    sols.append(m)
            if area[m[1]][m[0]] in ["1", " ", ".", "9"]:
                if m not in moves2:
                    moves2.append(m)
        for i in moves2:
            j = moves(i[0],i[1],area)  
            for k in j:
                if k not in moves3:
                    moves3.append(k)
        moves1 = moves3
    if len(sols) > 0:
        scores = {
            "1" : 3,
            " ": 6,
            "9": 36
        } 
        sols = sorted([((abs(i[1]-y)+abs(i[0]-x))/(scores[area[i[1]][i[0]]]),i[0],i[1]) for i in sols if not (i[0]==x and i[1]==y)])
        if len(sols) > 0:
            return [sols[0][1], sols[0][2]]
        else:
            return [x,y]
        
    else:
        return [x,y]

def good_eats(x,y,area,target,last_seen):
    sols = []
    moves1 = moves(x,y,area)
    for m in moves1:
        if area[m[1]][m[0]] in ["R","P","S"]:
            return m
    return last_seen[target]


width, height = [int(i) for i in input().split()]
area = [[]*width]*height
for i in range(height):
    row = input()  # one line of the grid: space " " is floor, pound "#" is wall
    area[i] = [j for j in row]
data = []
data_enemies = []
last_seen = {}
tf = {"R":"ROCK", "S":"SCISSORS","P":"PAPER"}
for i in range(20):
    data.append({'history':[], 'coolturns':0, 'target': 0, 'det':0})
    data_enemies.append({'coolturns':0, 'cooldown': 0})
turns = 200
while True:
    danger_cache = {}
    enemy_places = []
    for i in range(len(area)+5):
        enemy_row = []
        for j in range(len(area[0])+5):
            enemy_row.append("O")
        enemy_places.append(enemy_row)
    num_pacs = 0
    alive = 0
    my_score, opponent_score = [int(i) for i in input().split()]
    visible_pac_count = int(input())  # all your pacs and enemy pacs in sight
    if visible_pac_count > 0:
        turns -= 1
    for row in range(len(area)):
        for elem in range(len(area[0])):
            if area[row][elem] in ['R','P','S','T']:
                area[row][elem] = '.'
    ids = []
    for i in range(visible_pac_count):
        # pac_id: pac number (unique within a team)
        # mine: true if this pac is yours
        # x: position in the grid
        # y: position in the grid
        # type_id: unused in wood leagues
        # speed_turns_left: unused in wood leagues
        # ability_cooldown: unused in wood leagues
        pac_id, mine, x, y, type_id, speed_turns_left, ability_cooldown = input().split()
        pac_id = int(pac_id)
        mine = mine != "0"
        speed_turns_left = int(speed_turns_left)
        ability_cooldown = int(ability_cooldown)
        x = int(x)
        y = int(y)
        if mine:
            alive += 1
            ids.append(pac_id)
            data[pac_id]['pac_x'] = x
            data[pac_id]['pac_y'] = y
            data[pac_id]['type'] = type_id[0]
            data[pac_id]['cooldown'] = ability_cooldown
        if not mine: 
            area[y][x] = type_id[0] 
            data_enemies[pac_id]['sturns'] = speed_turns_left
            data_enemies[pac_id]['cooldown'] = ability_cooldown
            data_enemies[pac_id]['type'] = type_id[0]
            for i in range(len(enemy_places)):
                for j in range(len(enemy_places[0])):
                    if enemy_places[i][j] == pac_id:
                        enemy_places[i][j] = "O"
            enemy_places[y][x] = pac_id
            last_seen[pac_id] = [x,y]
        else:
            area[y][x] = "T"
        data[pac_id]['mine'] = mine
    if mine:
        for x,y in vision(data[pac_id]['pac_x'], data[pac_id]['pac_y'], area):
            area[y][x] = "."
    pellets = []
    visible_pellet_count = int(input())  # all pellets in sight
    for i in range(visible_pellet_count):
        # value: amount of points this pellet is worth
        x, y, value = [int(j) for j in input().split()]
        if value != 10:
            area[y][x] = str(value)
        else:
            area[y][x] = str(9)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    # MOVE <pacId> <x> <y>
    string = ""
    for row in area:
        str2 = ""
        for elem in row:
            str2 += str(elem) + " "
        #print(str2, file=sys.stderr)

    for pac_id in ids:
        if data[pac_id]['det'] > 0:
            if data_enemies[data[pac_id]['target']]['cooldown'] == 0 or counter(data_enemies[data[pac_id]['target']]['type']) != data[pac_id]['type']: 
                data[pac_id]['det'] = 0
                data[pac_id]['target'] = 0
                data[pac_id]['mode'] = 'moves'

    for pac_id in ids:
        if data[pac_id]['det'] > 0:
            data[pac_id]['mode'] = 'eats'
            data[pac_id]['det'] -= 1
        else:
            data[pac_id]['mode'] = 'moves'
    taken = [data[i]['target'] for i in ids if data[i]['mode'] == 'eats']

    enemies = [[i,j,enemy_places[j][i]] for j in range(height) for i in range(width) if enemy_places[j][i] != "O" and enemy_places[j][i] not in taken and (data_enemies[enemy_places[j][i]]['cooldown']>=5 or data_enemies[enemy_places[j][i]]['sturns'] > 0)]
    old_chasers = [i for i in ids if data[i]['mode']=='eats']
    chasers = []
    for enemy in enemies:
        dist = 4
        chaser = 9
        for pac_id in [i for i in ids if i not in old_chasers and i not in chasers]:
            d = abs(enemy[0] - data[pac_id]['pac_x']) + abs(enemy[1] - data[pac_id]['pac_y'])
            if d < dist:
                dist = d
                chaser = pac_id
        if chaser != 9:
            change = counter(area[enemy[1]][enemy[0]])
            if data[chaser]['cooldown'] == 0 and change == "R":
                data[chaser]['mode'] = "eats"
                if data[chaser]['type'] != "R":
                    string += "SWITCH {} ROCK eats={}|".format(chaser,data[chaser]['det'])
                else:
                    string += "SPEED {} eats={}|".format(chaser,data[chaser]['det'])
                data[chaser]['cooldown'] = 10
                data[chaser]['target'] = enemy[2]
                data[chaser]['det'] = 7
                chasers.append(chaser)
            elif data[chaser]['cooldown'] == 0 and change == "P":
                data[chaser]['mode'] = "eats"
                if data[chaser]['type'] != "P":
                    string += "SWITCH {} PAPER eats={}|".format(chaser,data[chaser]['det'])
                else:
                    string += "SPEED {} eats={}|".format(chaser,data[chaser]['det'])
                data[chaser]['cooldown'] = 10
                data[chaser]['target'] = enemy[2]
                data[chaser]['det'] = 7
                chasers.append(chaser)
            elif data[chaser]['cooldown'] == 0 and change == "S":
                data[chaser]['mode'] = "eats"
                if data[chaser]['type'] != "S":
                    string += "SWITCH {} SCISSORS eats={}|".format(chaser,data[chaser]['det'])
                else:
                    string += "SPEED {} eats={}|".format(chaser,data[chaser]['det'])
                data[chaser]['cooldown'] = 10
                data[chaser]['target'] = enemy[2]
                data[chaser]['det'] = 7
                chasers.append(chaser)
    if (my_score - opponent_score) > 0.25*turns and alive < 3:
        for pac_id in ids:
            data[pac_id]['mode'] = 'run'
        chasers = [] 
        string = ""    

    commanders = [i for i in ids if i not in chasers]
    
    if not ((my_score - opponent_score) > 0.25*turns and alive < 3):
        for pac_id in commanders:
            if pac_id not in old_chasers:
                data[pac_id]['mode'] = 'moves'

    for pac_id in commanders:
        if pac_id != commanders[-1]:
            ender = " {}|".format(data[pac_id]['mode'])
        else: 
            ender = " {}".format(data[pac_id]['mode'])
        if data[pac_id]['cooldown'] == 0:
            data[pac_id]['coolturns'] += 1
        if data[pac_id]['mode'] != 'run' and data[pac_id]['coolturns'] >= 10:
            string += "SPEED {}{}".format(pac_id,ender)
            data[pac_id]['coolturns'] = 0
        else:
            if len(data[pac_id]['history']) > 8:
                if data[pac_id]['history'][-1] == data[pac_id]['history'][-3] == data[pac_id]['history'][-5] == data[pac_id]['history'][-7]: 
                    flag = True
                    pac_x = data[pac_id]['pac_x']
                    pac_y = data[pac_id]['pac_y']
                    while flag:
                        x_delta = random.randint(-15,15)
                        y_delta = random.randint(-15,15)
                        if not (x_delta == 0 and y_delta == 0) and pac_x+x_delta > 0 and pac_y+y_delta > 0 and pac_x+x_delta < width-1 and pac_y+y_delta < height-1 and area[pac_y+y_delta][pac_x+x_delta] != '#':
                            flag = False

                    move = good_moves(pac_x+x_delta, pac_y+y_delta, area, 15)
                    string += "MOVE {} {} {}".format(pac_id, move[0], move[1]) + " ?" + ender
                else:
                    if data[pac_id]['mode'] == 'eats':
                        move = good_eats(data[pac_id]['pac_x'],data[pac_id]['pac_y'], area, data[pac_id]['target'], last_seen)
                        string += "MOVE {} {} {}".format(pac_id, move[0], move[1]) + " {} ".format(data[pac_id]['det']) + ender
                    elif data[pac_id]['mode'] == 'run':
                        donger = danger(data[pac_id]['pac_x'],data[pac_id]['pac_y'],area, enemy_places)
                        if donger[0] > .75 and data[pac_id]['cooldown'] == 0:
                            string += "SWITCH {} {}{}".format(pac_id, tf[counter(donger[1])], ender)
                        else:
                            move = good_runs(data[pac_id]['pac_x'],data[pac_id]['pac_y'], area, data_enemies, enemy_places)
                            string += "MOVE {} {} {}".format(pac_id, move[0], move[1]) + ender
                    else:
                        move = good_moves(data[pac_id]['pac_x'],data[pac_id]['pac_y'], area)
                        string += "MOVE {} {} {}".format(pac_id, move[0], move[1]) + ender

            else:
                if data[pac_id]['mode'] == 'eats':
                    move = good_eats(data[pac_id]['pac_x'],data[pac_id]['pac_y'], area, data[pac_id]['target'], last_seen)
                    string += "MOVE {} {} {}".format(pac_id, move[0], move[1]) + " {} ".format(data[pac_id]['det']) + ender
                elif data[pac_id]['mode'] == 'run':
                    print('run', pac_id, file=sys.stderr)
                    donger = danger(data[pac_id]['pac_x'],data[pac_id]['pac_y'],area, enemy_places)
                    if donger[0] > .75 and data[pac_id]['cooldown'] == 0:
                        string += "SWITCH {} {}{}".format(pac_id, tf[counter(donger[1])], ender)
                    else:
                        move = good_runs(data[pac_id]['pac_x'],data[pac_id]['pac_y'], area, data_enemies, enemy_places)
                        string += "MOVE {} {} {}".format(pac_id, move[0], move[1]) + ender
                else:
                    move = good_moves(data[pac_id]['pac_x'],data[pac_id]['pac_y'], area)
                    string += "MOVE {} {} {}".format(pac_id, move[0], move[1]) + ender

            data[pac_id]['history'].append([data[pac_id]['pac_x'],data[pac_id]['pac_y']])
    for enemy in data_enemies:
        if enemy['cooldown'] == 0:
            enemy['coolturns'] += 1
    print(string)