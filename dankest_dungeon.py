#Author: Erik Sandberg Co-author: Dalton Simac
import numpy as np
import sys
import time
import os
from dungeon_classes import *
from dungeon_functions import *


# define character attributes
starting_level = 1
start_health = 100
start_damage = 1
start_defense = 1
start_money = 0
start_potions = 1
first_floor = 1
start_score=0
start_exp=0
start_maxexp=10
start_keys = 0
try:
    local_high_score = int(np.loadtxt('local_high_score.txt'))
except:
    local_high_score = 0
    
# combine into one array for simplicity
character_starting_values = [starting_level,start_health,start_damage,start_defense, start_money, start_potions,first_floor,start_score,start_exp,start_maxexp,start_keys,local_high_score]


# define floor attributes
gridsize_x = np.random.randint(3,8)
gridsize_y = np.random.randint(3,8)
dimensions = [gridsize_x,gridsize_y]
starting_position = [np.random.randint(gridsize_x),np.random.randint(gridsize_y)]
player_position = starting_position
starting_stairs = [np.random.randint(gridsize_x),np.random.randint(gridsize_y)]
while starting_stairs == player_position:
    starting_stairs = [np.random.randint(gridsize_x),np.random.randint(gridsize_y)]


floor_starting_values = [gridsize_x,gridsize_y, np.random.randint(min(dimensions),max(dimensions)*2), [], starting_position, starting_position, [], starting_stairs]
floor = Floor(*floor_starting_values)
floor.generate_monsters()


#Initialize the game
os.system('clear')
print 'You are in the dankest of dungeons.'
time.sleep(1)
print 'What will you do?'
time.sleep(1)
print 'How will you get out?!'
time.sleep(1)
print 'A distant voice screams out for help...'
time.sleep(1)
print '----------------'
print 'Would you like to load a saved character?'
print '[Y] Yes'
print '[N] No'
yes_or_no = raw_input()
if yes_or_no == 'y':
    try:
        load_character = np.loadtxt('character_save.txt')
        user = player(*load_character.astype(int))
    except:
        print 'Unable to load character. Starting a new game.'
        user = player(*character_starting_values)
else:
     user = player(*character_starting_values)

os.system('clear')
print 'RUN'
time.sleep(2)
while True:
    os.system('clear')
    move_player(floor,user)
