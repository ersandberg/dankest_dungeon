#Author: Erik Sandberg Co-author: Dalton Simac
import numpy as np
import sys
import time
import os

# define starting_values

start_health = 100
start_damage = 1
start_defense = 1
start_money = 0
start_potions = 1
health_potion = 5 # heal 5 hit points
start_regen = 0
score = 0

#gridsize = 5
gridsize_x = np.random.randint(3,8)
gridsize_y = np.random.randint(3,8)
dimensions = [gridsize_x,gridsize_y]
first_floor = 1
starting_level = 1
starting_position = [np.random.randint(gridsize_x),np.random.randint(gridsize_y)]
player_position = starting_position
starting_stairs = [np.random.randint(gridsize_x),np.random.randint(gridsize_y)]
while starting_stairs == player_position:
    starting_stairs = [np.random.randint(gridsize_x),np.random.randint(gridsize_y)]
monster_list = [[5,2,'Blob',1,2,3],[12,4,'Giant spider',3,10,10],[10,3,'Zombie',2,5,4],[1,1,'Bat',1,1,2],[25,10,'Boss',10,200,30]]


# end of variable definitions
class player():
    def __init__(self,level,health,damage,defense,money,health_potions,floor,regen):
        self.level=level
        self.health=health
        self.damage=damage
        self.defense=defense
        self.money=money
        self.health_potions = health_potions
        self.floor=floor
        self.regen=regen
        self.monster_counter = 0
        self.score = 0
        self.exp = 0
        self.maxexp = 10 # exp needed to level up

    def gain_exp(self,value):
        self.exp += value
        print 'You gained ' + str(value) + ' experience.'
        #print 'your exp is', str(self.exp)
        if self.exp >= self.maxexp:
            self.level_up()
            self.exp = self.exp%self.maxexp
            self.maxexp += 5
        print str(self.maxexp - self.exp) + ' more experience to level up!'
        
    def lose_health(self,loss_of_health):
        if self.defense >= loss_of_health:
            return
        self.health -= (loss_of_health-self.defense)
        if self.health <= 0:
            endgame()
        print 'Your health is ' + str(self.health)
        
    def gain_health(self,gain_of_health):
        if self.health == 100:
            print 'You are at max health!'
            time.sleep(2)
            return
        self.health += gain_of_health
        print 'You healed for ' + str(gain_of_health)
        print 'Current health is now '+ str(self.health)

    def gain_money(self,gain_of_money):
        self.money += gain_of_money
    def lose_money(self,loss_of_money):
        self.money -= loss_of_money
    def lose_health_potion(self,number):
        self.health_potions -= number
        print 'You have ' + str(self.health_potions) + ' health potions left.'
        time.sleep(2)
    #def increase_regen(self):
    #    self.regen += 1
    #    while self.regen:
    #        time.sleep(10) #this completely pauses the game
    #        self.gain_health(self.regen)
    def level_up(self):
        self.level += 1
        self.damage +=1
        self.defense +=1
        #self.increase_regen()
        self.add_score(100) # level gives 100 points
        print 'You reached level ', str(self.level) + '! You have grown in strength.'
        time.sleep(2)
    def defeat_monster(self,value):
        self.monster_counter +=1
        self.gain_exp(value)
        #if self.monster_counter%2 == 0:
            #self.level_up()
    def add_score(self,points):
        self.score += points

class Floor():
    def __init__(self,gridsize_x,gridsize_y,number_of_monsters,monster_positions,starting_position,player_position, sensei_position,stair_position):
        self.gridsize_x = gridsize_x
        self.gridsize_y = gridsize_y
        self.number_of_monsters = number_of_monsters
        self.monster_positions = monster_positions
        self.starting_position = starting_position
        self.player_position = player_position
        self.sensei_position = sensei_position
        self.stair_position = stair_position

    def generate_monsters(self):
        for i in range(self.number_of_monsters):
            self.monster_positions.append([np.random.randint(self.gridsize_x),np.random.randint(gridsize_y)])


class monster():
    def __init__(self,health,damage,name,value,score,experience):
        self.health = health
        self.damage = damage
        self.name = name
        self.value = value
        self.score = score
        self.experience = experience
        
    def lose_health(self,loss_of_health):
        self.health -= loss_of_health
        

class Sensei():
    def __init__(self,available_health_potions,teach_offense, teach_defense):
        self.available_health_potions = available_health_potions
        self.teach_offense = teach_offense
        self.teach_defense = teach_defense

    def lose_health_potion(self):
        if user.money < 1:
            print 'You do not have enough money. '
            return
        if self.available_health_potions > 0:
            user.health_potions +=1
            user.money -= 1 # cost of potion
            print 'You now have ' + str(user.health_potions) + ' health potions. May they serve you well, adventurer. '
        else:
            print 'I have no more potions for you, small grasshopper. '
        self.available_health_potions -= 1
        

    def lose_teach_offense(self):
        if user.money < 2:
            print 'You do not have enough money. '
            return
        if self.teach_offense > 0:
            user.damage += 1
            user.money -= 2 # cost of learning
            print 'You learn quickly. Your damage is now ' + str(user.damage) + '.' 
        else:
            print 'You have gained all of my offensive knowledge. '
        self.teach_offense -= 1

    def lose_teach_defense(self):
        if user.money < 2:
            print 'You do not have enough money. '
            return
        if self.teach_defense > 0:
            user.defense += 1
            user.money -= 2 # cost of learning
            print 'Well done, light mongoose. You now have ' + str(user.defense) + ' defense. '
        else:
            print 'You have already learned more defensive tactics than I, young master. '
            self.teach_defense -= 1



starting_floor = Floor(gridsize_x,gridsize_y, np.random.randint(min(dimensions),max(dimensions)*2), [], starting_position, starting_position, [], starting_stairs)
starting_floor.generate_monsters()

user = player(starting_level,start_health,start_damage,start_defense, start_money, start_potions,first_floor,start_regen)
floor = starting_floor


def draw(name): # name_of_monster= enemy.name
    if name == 'Stairs':
        print ''
        print ''
        print '      __'
        print '_____|'
        time.sleep(2)
        os.system('clear')
        print ''
        print '         __'
        print '      __|'    
        print '_____|'
        time.sleep(2)
        os.system('clear')
        print '            _______'
        print '         __|'
        print '      __|'    
        print '_____|'
        print ''
        print 'You ascended to floor ' + str(user.floor) +'.'
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
    if name == 'Boss':
        print '???'
        print '???'
        print '???'
        print ''
        print ''


def header():
    print 'Floor: ', user.floor, 'Level: ', user.level, 'Experience: ', str(user.exp) + '/' + str(user.maxexp), 'Damage: ', user.damage, 'Defense: ', user.defense, 'Health: ', user.health, 'Gold: ', user.money, 'Health potions: ', user.health_potions
    print '---------------------------------------------------------------------------------------------------------'
    print 'High score: ', user.score
    print ''
    print ''
    
def legend():
    print 'Player = X , Stair = s , ??? = o'
def victory():
    print 'You defeated the boss! You win!'
    print 'High score: ', user.score
    time.sleep(3)
    os.system('clear')
    sys.exit()
def endgame():
    os.system('clear')
    print 'You ran out of health.'
    print 'GAME'
    print 'OVER'
    print 'High score: ', user.score
    time.sleep(3)
    os.system('clear')
        
def display(gridsize_x=gridsize_x, gridsize_y=gridsize_y):
    # create base grid
    top   = ' _ '*gridsize_x
    row   = '|_|'*gridsize_x
    array = []
    for i in range(gridsize_y):
        array.append(row)
    
    # place monster markers
    for position in floor.monster_positions:
        x = position[0]
        y = position[1]
        listed = list(array[y])
        listed[3*x+1] = 'o'
        array[y] = "".join(listed)

    # place sensei marker
    try:
        x = floor.sensei_position[0]
        y = floor.sensei_position[1]
        listed = list(array[y])
        listed[3*x+1] = 'o'
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
    x = floor.stair_position[0]
    y = floor.stair_position[1]
    listed = list(array[y])
    listed[3*x+1] = 's'
    array[y] = "".join(listed)
    
    print top
    for i in range(gridsize_y):
        print array[i]
    print ''
    print ''





    

    
    



def move_player(floor):
    
    header()
    legend()
    display(gridsize_x,gridsize_y)
    print 'Which way would you like to move?'
    print '[A] Left'
    print '[D] Right'
    print '[W] Up'
    print '[S] Down'

    move = raw_input()
    if move == 'a': # left
        if floor.player_position[0] != 0:
            floor.player_position[0] -= 1
            if floor.player_position in floor.monster_positions:
                fight()
            if floor.player_position == floor.stair_position:
                use_stairs()
            if floor.player_position == floor.sensei_position:
                use_sensei()
        else:
            print "You hit a wall... Try again. "
            time.sleep(2)
            os.system('clear')
            move_player(floor)
            
    if move == 'd': # right
        if floor.player_position[0] != floor.gridsize_x-1:
            floor.player_position[0] += 1
            if floor.player_position in floor.monster_positions:
                fight()
            if floor.player_position == floor.stair_position:
                use_stairs()
            if floor.player_position == floor.sensei_position:
                use_sensei()
        else:
            print "That's a WALL, numbskull! Try again. "
            time.sleep(2)
            os.system('clear')
            move_player(floor)
            
    if move == 'w': # up
        if floor.player_position[1] !=0:
            floor.player_position[1] -= 1
            if floor.player_position in floor.monster_positions:
                fight()
            if floor.player_position == floor.stair_position:
                use_stairs()
            if floor.player_position == floor.sensei_position:
                use_sensei()
        else:
            print "Another wall. Rats! Try again. "
            time.sleep(2)
            os.system('clear')
            move_player(floor)
    if move == 's': # down
        if floor.player_position[1] != floor.gridsize_y-1:
            floor.player_position[1] += 1
            if floor.player_position in floor.monster_positions:
                fight()
            if floor.player_position == floor.stair_position:
                use_stairs()
            if floor.player_position == floor.sensei_position:
                use_sensei()
        else:
            print "You realize you're trying to walk through a wall, right? Try again. "
            time.sleep(2)
            os.system('clear')
            move_player(floor)
            
def use_stairs():
    user.floor += 1
    user.score += 50
    floor.number_of_monsters = np.random.randint(3,5)
    floor.monster_positions = []
    floor.generate_monsters()
    floor.stair_position = [np.random.randint(gridsize_x),np.random.randint(gridsize_y)]
    
    if user.floor%2 ==0:
        floor.sensei_position = [np.random.randint(gridsize_x),np.random.randint(gridsize_y)]
    else:
        floor.sensei_position = []

    while floor.stair_position == floor.player_position or floor.stair_position == floor.sensei_position:
        floor.stair_position = [np.random.randint(gridsize_x),np.random.randint(gridsize_y)]
        
    os.system('clear')

    print 'You stumbled upon a raggedy staircase. You naively decide to ascend.'
    time.sleep(2)
    os.system('clear')
    # animation
    draw('Stairs')
 
    time.sleep(2)


    
def use_sensei():
    os.system('clear')
    header()
    draw('Sensei')
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
        sensei.lose_health_potion()
        time.sleep(2)
        use_sensei()
    if action == '2':
        sensei.lose_teach_offense()
        time.sleep(2)
        use_sensei()
    if action == '3':
        sensei.lose_teach_defense()
        time.sleep(2)
        use_sensei()
    if action =='4':
        print 'You leave the sensei alone. He whispers quietly to himself: "Finally..."'
        time.sleep(2.5)
        return





















def fight():

    # initiate fight
    random = np.random.randint(len(monster_list))
    enemy = monster(*monster_list[random])

    while True:
        os.system('clear')
        header()
        print 'You are fighting a ' + str(enemy.name) + '!'
        print str(enemy.name) + ' has ' + str(enemy.health) + ' health!'
        if user.defense >= enemy.damage:
            print str(enemy.name) + ' deals 0 damage. '
        else:
            print str(enemy.name) + ' deals ' + str(enemy.damage - user.defense) + ' damage!'
        print ''
        draw(enemy.name)
        # pick action
        print 'What will you do?'
        print '[1] Fight'
        print '[2] Use potion'
        print '[3] Run'
        action = raw_input()

        if action == '1': # fight monster
            user.lose_health(enemy.damage)
            enemy.lose_health(user.damage)
            if enemy.health < 1:
                print str(enemy.name) + ' has 0 health!'
            else:
                print str(enemy.name) + ' has ' + str(enemy.health) + ' health remaining!'
        if action == '2': # use potion
            if user.health_potions and user.health !=100:
                user.gain_health(health_potion)
                user.lose_health_potion(1)
            else:
                print 'Failed to use health potion. (Either no health potions or you are at max health.)'
                time.sleep(2)
        if action == '3': # run away
            print 'You ran from the ' + str(enemy.name)
            return
            
        if enemy.health <= 0: # defeated enemy
            os.system('clear')
            header()
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
            if enemy.name == 'Boss':
                victory()
            time.sleep(3)
            return


#Initialize the game
os.system('clear')
print 'You are in the dankest of dungeons.'
time.sleep(1)
print 'What will you do?'
time.sleep(1)
print 'How will you get out?!'
time.sleep(1)
print 'A voice calls out from the darkness...'
time.sleep(1)
print '"Would you like to play a game?"'
print '-------'
print '[1] Yes'
print '[2] No'
yes_or_no = raw_input()
if yes_or_no == '2':
    sys.exit()
#print 'How big should the dungeons be? Enter a number between 3 and 10'
#gridsize = int(raw_input())
os.system('clear')
print 'RUN'
time.sleep(2)
while True:
    os.system('clear')
    move_player(floor)
