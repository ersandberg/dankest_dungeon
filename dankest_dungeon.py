#Author: Erik Sandberg Co-author: Dalton Simac
import numpy as np
import sys
import time
import os
from dungeon_classes import *
from dungeon_functions import *
from dankest_storyline import *


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
character_starting_values = [starting_level,start_health,start_damage,start_defense, start_money, start_potions,first_floor,start_score,start_exp,start_maxexp,start_keys]


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

outdoors = Outdoors()


#Initialize the game
intro()
user = player(*load_character(character_starting_values).astype(int))

'''
print '----------------'
print 'Would you like to load a saved character?'
print '[Y] Yes'
print '[N] No'
user = player(*load_character(character_starting_values))
yes_or_no = ''
while yes_or_no == '': # in case person spams return during intro
    yes_or_no = raw_input()
    if yes_or_no == 'y' or yes_or_no == 'Y':
        try:
            load_character = np.loadtxt('character_save.txt')
            user = player(*load_character.astype(int))
            print 'Loading saved character. '
        except:
            print 'Unable to load character. Starting a new game.'
            user = player(*character_starting_values)
    if yes_or_no == 'n' or yes_or_no == 'N':
        user = player(*character_starting_values)
        print 'Starting a new character.'
        time.sleep(2)
'''
user.local_high_score = local_high_score
os.system('clear')
print 'RUN'
time.sleep(2)

user.in_dungeon = False # For testing
user.outside = True # for testing
while user.in_dungeon: # dungeon sequence
    os.system('clear')
    move_player(floor,user)
outside_intro()
while user.outside: # outdoor sequence
    os.system('clear')
    running(outdoors,user)
while user.archery:
    archery_intro()
        

