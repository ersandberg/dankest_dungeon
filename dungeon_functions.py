#Erik Sandberg
#Functions used in dankest_dungeon.py
import numpy as np
import sys
import time
import os
from dungeon_classes import *
obstacle_damage = 15

def use_stairs(floor,user):
    user.floor += 1
    user.score += 50
    floor.number_of_monsters = np.random.randint(min(floor.dimensions),max(floor.dimensions)*2) # FIX THIS?
    floor.monster_positions = []
    floor.generate_monsters()
    floor.stair_position = [np.random.randint(floor.gridsize_x),np.random.randint(floor.gridsize_y)]
    if user.floor%2 ==0:
        floor.sensei_position = [np.random.randint(floor.gridsize_x),np.random.randint(floor.gridsize_y)]
    else:
        floor.sensei_position = []

    while floor.stair_position == floor.player_position or floor.stair_position == floor.sensei_position:
        floor.stair_position = [np.random.randint(floor.gridsize_x),np.random.randint(floor.gridsize_y)]
    if user.floor == 5: # last level, no stairs, only 1 guard monster
        floor.stair_position = []
        floor.door_position = [0,0]
        floor.monster_positions = [[0,0]]
    
    os.system('clear')

    #time.sleep(2)
    os.system('clear')
    # animation
    draw('Stairs',user) 
    time.sleep(2)


    
def use_sensei(user):
    os.system('clear')
    header(user)
    draw('Sensei',user)
    sensei = Sensei(3,1,1)
    print ' You encounter an old man with several strands of hair on his chin. '
    print ' He says he can supply you with things you may need. '
    print ''
    print ''
    print ' What would you like to do? '
    print '[1] Buy health potion (1 gold).'
    print '[2] Increase damage (2 gold).'
    print '[3] Increase defense (2 gold).'
    print '[4] Leave.'
    action = raw_input()

    if action == '1':
        sensei.lose_health_potion(user)
        time.sleep(2)
        use_sensei(user)
    if action == '2':
        sensei.lose_teach_offense(user)
        time.sleep(2)
        use_sensei(user)
    if action == '3':
        sensei.lose_teach_defense(user)
        time.sleep(2)
        use_sensei(user)
    if action =='4':
        print 'You leave the sensei alone. He whispers quietly to himself: "Finally..."'
        time.sleep(2.5)
        return



def fight(floor,user):
    
    # initiate fight
    random = np.random.randint(len(floor.monster_list))
    enemy = monster(*floor.monster_list[random])
    if user.floor == 5: # boss
        enemy = monster(*floor.monster_list[-1])
    while True:
        os.system('clear')
        header(user)
        print 'You are fighting a ' + str(enemy.name) + '!'
        print str(enemy.name) + ' has ' + str(enemy.health) + ' health!'
        if user.defense >= enemy.damage:
            print str(enemy.name) + ' deals 0 damage. '
        else:
            print str(enemy.name) + ' deals ' + str(enemy.damage - user.defense) + ' damage!'
        print ''
        draw(enemy.name,user)
        # pick action
        print 'What will you do?'
        print '[1] Fight'
        print '[2] Use potion'
        print '[3] Run'
        action = raw_input()

        if action == '1': # fight monster
            user.lose_health(enemy.damage)
            if user.health <= 0:
                endgame(user)
            enemy.lose_health(user.damage)
            if enemy.health < 1:
                print str(enemy.name) + ' has 0 health!'
            else:
                print str(enemy.name) + ' has ' + str(enemy.health) + ' health remaining!'
        if action == '2': # use potion
            if user.health_potions and user.health !=100:
                user.gain_health(20) # value of health potion
                user.lose_health_potion(1)
            else:
                print 'Failed to use health potion. (Either no health potions or you are at max health.)'
                time.sleep(2)
        if action == '3': # run away
            if user.floor == 5:
                print "There is nowhere to run on floor " + str(user.floor) +"!"
                print "While you were trying to escape, " + str(enemy.name) + " bandaged its wounds! Doh!"
                time.sleep(2)
                fight(floor,user)
            print 'You ran from the ' + str(enemy.name)
            return user
            
        if enemy.health <= 0: # defeated enemy
            os.system('clear')
            header(user)
            print 'Enemy killed!'
            print 'You gained ' + str(enemy.value) + ' gold!'
            user.defeat_monster(enemy.experience)
            #user.gain_exp(enemy.experience)
            user.gain_money(enemy.value)
            user.add_score(enemy.score)
            print ''
            print 'VICTORY!!'
            print ''
            # remove monster from the floor
            counter = 0
            for position in floor.monster_positions:
                if position == floor.player_position:
                    del floor.monster_positions[counter]
                counter += 1
            #if enemy.name == 'Guard':
                #print 'You found a KEY.'
                #user.keys +=1
            time.sleep(3)
            return user



def move_player(floor,user):
    
    header(user)
    legend(user)
    display(floor.gridsize_x,floor.gridsize_y,floor)
    print 'What would you like to do?'
    print '[w] Move up'
    print '[a] Move left'
    print '[s] Move down'
    print '[d] Move right'
    print '[p] Use health potion'
    print '[c] Read instructions'
    print '[z] Quit'
    print '[x] Save character'
    

    move = raw_input()
    if move == 'p' or move == 'P':
        if user.health_potions and user.health !=100:
            user.gain_health(20) # value of health potion
            user.lose_health_potion(1)
        else:
            print 'Failed to use health potion. (Either no health potions or you are at max health.)'
        time.sleep(2)

    if move == 'c' or move == 'C':
        draw('Instructions',user)
        goback = raw_input('Press any key, then return to go back. ')
        if goback:
            return
        
    if move == 'z' or move == 'Z': # quit
        print "You don't really want to quit the game, do you? :("
        print '[Y] Yes, I want to quit. '
        print "[N] No, I want to keep playing. I was only kidding. "
        yes_or_no = raw_input()
        if yes_or_no == 'y' or yes_or_no == 'Y':
            sys.exit()

    if move == 'x' or move == 'X': # save
        np.savetxt('character_save.txt',[user.level,user.health,user.damage,user.defense,user.money,user.health_potions,user.floor,user.score,user.exp,user.maxexp,user.keys,user.local_high_score])
        #np.savetxt('floor_save.txt', [floor.gridsize_x,floor.gridsize_y,floor.number_of_monsters,floor.monster_positions,floor.starting_position,floor.player_position,floor.sensei_position,floor.stair_position]) # attempt to save floor
        print 'Save successful'
        time.sleep(2)
    
    if move == 'a' or move == 'A': # left
        if floor.player_position[0] != 0:
            floor.player_position[0] -= 1

            if floor.player_position == floor.stair_position:
                use_stairs(floor,user)
            if floor.player_position == floor.sensei_position:
                use_sensei(user)
            if floor.player_position in floor.monster_positions:
                fight(floor,user)
            if floor.player_position == floor.door_position:
                #fight(floor,user) # Is this what caused 2 door Gaurds?
                leave_dungeon(floor,user)
        else:
            print "You hit a wall... Try again. "
            time.sleep(2)
            os.system('clear')
            move_player(floor,user)
            
    if move == 'd' or move == 'D': # right
        if floor.player_position[0] != floor.gridsize_x-1:
            floor.player_position[0] += 1
            if floor.player_position in floor.monster_positions:
                fight(floor,user)
            if floor.player_position == floor.stair_position:
                use_stairs(floor,user)
            if floor.player_position == floor.sensei_position:
                use_sensei(user)
            if floor.player_position == floor.door_position:
                #fight(floor,user)
                leave_dungeon(floor,user)
        else:
            print "That's a WALL, numbskull! Try again. "
            time.sleep(2)
            os.system('clear')
            move_player(floor,user)
            
    if move == 'w' or move == 'W': # up
        if floor.player_position[1] !=0:
            floor.player_position[1] -= 1
            if floor.player_position in floor.monster_positions:
                fight(floor,user)
            if floor.player_position == floor.stair_position:
                use_stairs(floor,user)
            if floor.player_position == floor.sensei_position:
                use_sensei(user)
            if floor.player_position == floor.door_position:
                #fight(floor,user)
                leave_dungeon(floor,user)
        else:
            print "Another wall. Rats! Try again. "
            time.sleep(2)
            os.system('clear')
            move_player(floor,user)
    if move == 's' or move == 'S': # down
        if floor.player_position[1] != floor.gridsize_y-1:
            floor.player_position[1] += 1
            if floor.player_position in floor.monster_positions:
                fight(floor,user)
            if floor.player_position == floor.stair_position:
                use_stairs(floor,user)
            if floor.player_position == floor.sensei_position:
                use_sensei(user)
            if floor.player_position == floor.door_position:
                #fight(floor,user)
                leave_dungeon(floor,user)
        else:
            print "You realize you're trying to walk through a wall, right? Try again. "
            time.sleep(2)
            os.system('clear')
            move_player(floor,user)

def grab_item(outdoors,user):
    print 'You grabbed an item.'
    r = np.random.rand()
    user.add_score(75)
    if r < .6:
        user.gain_money(1)
        print 'The item was a gold piece! Not bad!'
    if r >= .6 and r <= .85:
        user.health_potions += 1
        print 'The item was a health potion! Nice!'
    if r > .85:
        user.superboots = True
        print 'YOU FOUND SUPERBOOTS! You can easily escape now!'
    time.sleep(2)
def hit_obstacle(outdoors,user):
    user.lose_health(obstacle_damage+user.defense) # defense doesn't stop this damage
    print 'You hit an obstacle. Ouch, that hurts!'
    if user.health <= 0:
        endgame(user)
    time.sleep(2)
def running(outdoors,user): # analagous to "move_player" for inside dungeon
    header(user)
    display(outdoors.gridsize_x,outdoors.gridsize_y,outdoors)
    print 'You are on the run from evil! '
    print 'You can now jump over obstacles. '
    print 'Pick up objects while running, or just escape! '
    print ''
    print ''
    print 'What would you like to do?'
    print '[w] Move up  '
    print '[s] Move down'
    print '[d] Jump   '
    if user.superboots:
        print '[B] Use superboots to outrun the evil!'
    
    obst_num = np.random.randint(1,3)
    item_rand = np.random.rand()
    if item_rand > .9:
        item_num = 1
    else:
        item_num = 0

    move = raw_input()

    if move == '':
        outdoors.advance_terrain(obst_num,item_num) # create obstacles & items      
        if outdoors.player_position in outdoors.item_locations:
            grab_item(outdoors,user)
        if outdoors.player_position in outdoors.obstacle_locations:
            hit_obstacle(outdoors,user)
            
    if move == 'w' or move == 'W': # up
        outdoors.advance_terrain(obst_num,item_num) 
        if outdoors.player_position[1] !=0:
            outdoors.player_position[1] -= 1
            if outdoors.player_position in outdoors.item_locations:
                grab_item(outdoors,user)
            if outdoors.player_position in outdoors.obstacle_locations:
                hit_obstacle(outdoors,user)
        else:
            print "Can't go out of bounds! Try again. "
            time.sleep(2)
            os.system('clear')
            running(outdoors,user)

            
    if move == 's' or move == 'S': # down
        outdoors.advance_terrain(obst_num,item_num) # create obstacles & items

        if outdoors.player_position[1] != outdoors.gridsize_y-1:
            outdoors.player_position[1] += 1
            if outdoors.player_position in outdoors.item_locations:
                grab_item(outdoors,user)
            if outdoors.player_position in outdoors.obstacle_locations:
                hit_obstacle(outdoors,user)
            
        else:
            print "You realize you're trying to walk out of bounds, right? Try again. "
            time.sleep(2)
            os.system('clear')
            running(outdoors,user)
        

    if move == 'd' or move == 'D': # jump over obstacle
        outdoors.advance_terrain(obst_num,item_num)
        outdoors.advance_terrain(obst_num,item_num)
        if outdoors.player_position in outdoors.item_locations:
            grab_item(outdoors,user)
        if outdoors.player_position in outdoors.obstacle_locations:
            hit_obstacle(outdoors,user)        

    if move == 'b' or move == 'B':
        while outdoors.player_position[0] < outdoors.gridsize_x-1:
            outdoors.player_position[0] +=1
            outdoors.advance_terrain(0,0)
            os.system('clear')
            display(outdoors.gridsize_x,outdoors.gridsize_y,outdoors)
            time.sleep(0.5)
        #os.system('clear')
        #print 'You escaped the evil for good!'
        #print 'Nice work, Hotshot! '
        #time.sleep(3)
        #return #
        leave_outdoors(outdoors,user)
    

def display(gridsize_x, gridsize_y,floor):
    # create base grid
    top   = ' _ '*floor.gridsize_x
    row   = '|_|'*floor.gridsize_x
    array = []
    for i in range(floor.gridsize_y):
        array.append(row)

    try: #floor here would be outdoors
        for position in floor.obstacle_locations:
            x = position[0]
            y = position[1]

            listed = list(array[y])
            listed[3*x+1] = 'A'
            if x < 1: #do not display if at x=0, cannot hit that obstacle
                listed[3*x+1] = '_'
            array[y] = "".join(listed)
    except:
        pass

    try: #floor here would be outdoors
        for position in floor.item_locations:
            x = position[0]
            y = position[1]
            listed = list(array[y])
            listed[3*x+1] = 'i'
            if x < 1: #do not display if at x=0, cannot hit that obstacle
                listed[3*x+1] = '_'
            array[y] = "".join(listed)
    except:
        pass
    # place monster markers
    try:
        if len(floor.monster_positions) != 1:
            for position in floor.monster_positions:
                x = position[0]
                y = position[1]
                listed = list(array[y])
                listed[3*x+1] = 'o'
                array[y] = "".join(listed)
        else:
            x = floor.monster_positions[0][0]
            y = floor.monster_positions[0][1]
            listed = list(array[y])
            listed[3*x+1] = 'o'
            array[y] = "".join(listed)
    except:
        pass

        
    # place sensei marker
    try:
        x = floor.sensei_position[0]
        y = floor.sensei_position[1]
        listed = list(array[y])
        listed[3*x+1] = 'w'
        array[y] = "".join(listed)
    except:
        pass
    
    # place player marker
    x = floor.player_position[0]
    y = floor.player_position[1]
    listed = list(array[y])
    listed[3*x+1] = 'X'
    array[y] = "".join(listed)

    # place stair marker
    try:
        x = floor.stair_position[0]
        y = floor.stair_position[1]
        listed = list(array[y])
        listed[3*x+1] = 's'
        array[y] = "".join(listed)
    except:
        pass
    #place door marker
    try:
        x = floor.door_position[0]
        y = floor.door_position[1]
        listed = list(array[y])
        listed[3*x+1] = 'd'
        array[y] = "".join(listed)
    except:
        pass
    
    print top
    for i in range(floor.gridsize_y):
        print array[i]
    print ''
    print ''



def draw(name,user): # name_of_monster= enemy.name
    if name == 'Stairs':
        print 'You stumbled upon a raggedy staircase. You naively decide to ascend.'
        print '            '
        print '            '
        print '            '
        print '            '
        print '  o         '
        print ' /|\    ____'
        print '_/ \___|    '
        time.sleep(1.5)
        os.system('clear')
        print 'You stumbled upon a raggedy staircase. You naively decide to ascend.'
        print '                   '
        print '                   '
        print '                   '
        print '          o        '
        print '         /|\   ____'
        print '        _/ \__|    '    
        print '_______|'
        time.sleep(1.5)
        os.system('clear')
        print 'You stumbled upon a raggedy staircase. You naively decide to ascend.'
        print '                             '
        print '                             '
        print '                 o           '
        print '                /|\  _______ '
        print '               _/ \_|'
        print '        ______|'    
        print '_______|'
        print ''
        time.sleep(1.5)
        os.system('clear')
        print 'You stumbled upon a raggedy staircase. You naively decide to ascend.'
        print '                             __ '
        print '                       o    |  |'
        print '                      /|\   | .|'
        print '                     _/ \___|__|'
        print '               _____|'
        print '        ______|'    
        print '_______|'
        print ''
        print 'You reached floor ' + str(user.floor) +'.'
    if name == 'Sensei':
        print '     _     '
        print '   /   \   '
        print '  /     \  '
        print ' | 0  0  | '
        print ' (   &   ) '
        print '  \ --- /  '
        print '   ( | )   '
        print '    (|)    '
        print '     v     '
        print ''
        print ''
    if name == 'Blob':
        print '   _______   '
        print '  /       \  '
        print ' ( .\   /. ) '
        print ' (         ) '
        print ' (  (___)  ) '
        print '  (       )  '
        print '   vvvvvvv   '
        print '             '
        print '             '
        print '             '
    if name == 'Giant spider':
        print '       /\  /\__wwwwww__/\  /\        '
        print '      /  \/ /          \ \/  \       '
        print '     /    \/   oo  oo   \/    \      '
        print '    /  /\  |            |  /\  \     '
        print '   /  /  \ |  {vvvvvv}  | /  \  \    '
        print '  /  /    \|  {^^^^^^}  |/    \  \   '
        print ' /  /     / \__________/ \     \  \  '
        print '         /                \          '
        print '                                     '
        print '                                     '
        print '                                     '
    if name == 'Zombie':
        print '   .-^---^-.   '
        print '  /         \  '
        print ' [  x    x   ] '
        print ' [    ..     ] '
        print ' [   _ _ _   ] '
        print '  \ |m|m|m| /  '
        print '    -------    '
        print '               '
        print '               '
    if name == 'Bat':
        print '    /^\               /^\      '
        print '   /   \    _____    /   \     '
        print '  /     \  /     \  /     \    '
        print ' /   /\  \/ o   o \/  /\   \   '
        print ' \  /  \./|       |\./  \  /   '
        print '  \/       \.vwv./       \/    '
        print '                               '
        print '                               '
        print '                               ' 
    if name == 'Guard':
        print '        . .    . .    '
        print '      ./.  \  /  .\.  '
        print '      ?   __\/_    ?  '
        print '         /  /  \      '
        print '      .-/-"""""-\-.   '
        print '      "           "   '
        print '     "_____________"  '
        print '     "__|pq|_|pq|__"  '
        print '     "     ...     "  '
        print '     "             "  '
        print '      "   |= =|   "   '
        print '       "         "    '
        print '        ""-----""     '
        print '                      '
        print '                      '
    if name == 'Instructions':
        os.system('clear')
        print ' GOAL: Get to floor five and escape the dungeon. '
        print ' You will need to get stronger to leave the fifth floor. '
        print ' Fight monsters to get stronger. '
        print ' Learn from old wise men to get stronger. '
        print ' Take the stairs to fight more monsters. '
        print ' You lose health when fighting monsters. '
        print ' Use health potions to get back some health if you need to. '
        print ' If your health reaches 0, you lose! '
        print ' '
        
def leave_outdoors(floor,user):
    os.system('clear')
    header(user)
    print 'You were able to escape the fields. '
    time.sleep(2)
    user.outside=False
    user.archery=True
def leave_dungeon(floor,user):
    os.system('clear')
    header(user)
    print 'You make it out of the dungeon alive'
    time.sleep(2)
    user.in_dungeon = False
    user.outside = True
    #victory(user)

def header(user):
    print 'Floor: ', user.floor, 'Level: ', user.level, 'Experience: ', str(user.exp) + '/' + str(user.maxexp), 'Damage: ', user.damage, 'Defense: ', user.defense, 'Health: ', user.health, 'Gold: ', user.money, 'Health potions: ', user.health_potions
    print '---------------------------------------------------------------------------------------------------------'
    print 'Previous high score: ', user.local_high_score
    print 'Your score: ', user.score 
    print ''
    print ''
    
def legend(user):
    if user.floor == 5:
        print 'USE THE DOOR!'
    #if user.floor == 5:
        #print 'Player = X , Stairs = s , Monsters = o , Wise old men = w , DOOR = d '
    print 'Player = X , Stairs = s , Monsters = o , Wise old men = w , door = d'
def victory(user):
    print 'High score: ', user.score
    #np.savetxt('character_save.txt', ) delete character save file
    np.savetxt('local_high_score.txt', [user.score])
    time.sleep(3)
    os.system('clear')
    sys.exit()
def endgame(user):
    os.system('clear')
    print 'You ran out of health.'
    print 'GAME'
    print 'OVER'
    print 'High score: ', user.score
    time.sleep(3)
    np.savetxt('local_high_score.txt', [user.score])
    os.system('clear')
    sys.exit()
