#Erik Sandberg
#Dankest Dungeon story line
import os
import time

def p(): # press a key
    print ''
    print ''
    print ''
    print ''
    print ''
    print ''
    print ''
    print 'Press [return] to continue'
    key = raw_input()
    os.system('clear')

def cliffs():
    print '                                   o   '
    print '                                   /|\ '
    print '____________________________._._.__l|  '
    print '       .               .    {   }    ] '
    print '                 .          {   }    ] '
    print '                      .     {   }    ] '
    print '      .                     {   }    ] '
    print '            @               {   }    ] '
    print '                    .       {   }    ] '
    print '               .            {   }    ] '
    print '       v                    {   }    ] '
    print '                 ..         {   }    ] '
def cliffs2():
    print '                                " @$%! "         '
    print '                             \o/         '
    print '____________________________. | .____  '
    print '                            {/ \}    ] '
    print '        ~          .        {   }    ] '
    print '       .                 .  {   }    ] '
    print '                    v       {   }    ] '
    print '              .             {   }    ] '
    print '     .                .     {   }    ] '
    print '                 .          {   }    ] '
    print '         .                  {   }    ] '    
def cliffs3():
    print '                                       '
    print '                                       '
    print '____________________________.   .____  '
    print '        .                   {   }    ] '
    print '   .          .      o      {   }    ] '
    print '   .     (                  {   }    ] '
    print '                 .      ;   {   }    ] '
    print '          .                 {   }    ] '
    print '                            {   }    ] '
    print '   .               .        {\o/}    ] '
    print '                            { | }    ] '    

def intro():
    os.system('clear')
    print 'Ouch... my head really hurts...'
    print ''
    print ''
    p()
    print 'God, what even happened?'
    print ''
    print ''
    p()
    print 'Where the hell am I?'
    print ''
    print ''
    p()
    print 'Last thing I remember was... '
    print ''
    print ''
    p()
    print 'Last thing I remember was... '
    print 'Damn. '
    print ''
    p()
    print 'Last thing I remember was... '
    print 'Damn. '
    print '.'
    p()
    print 'Last thing I remember was... '
    print 'Damn. '
    print '..'
    p()
    print 'Last thing I remember was... '
    print 'Damn. '    
    print '...'
    p()
    print 'I remember! I was walking back from the cliffs.'
    cliffs()
    p()
    print 'But a giant hole in the ground had been covered up!'
    cliffs()
    p()
    print 'I fell through it... but how far down did I go?'
    cliffs2()
    p()
    print 'Best I can remember - really far. '
    cliffs3()
    p()
    print ''
    p()
    print "And now I'm here. God knows where."
    p()
    print "It's a little chilly down here... "
    p()
    print '... and dank. '
    p()
    print 'The floor is tile. Feels like some sort of dungeon.'
    p()
    print '"The dank dungeon. "'
    p()
    print 'Hehehe.. '
    p()
    print 'Oooh! The "Dankest_dungeon" '
    p()
    print "Yeah, yeah. That's got a nice ring to it. "
    p()
    print 'I suppose I should light a match, huh? '
    p()
    time.sleep(2)
    print ' T H E   D A N K E S T   D U N G E O N '
    time.sleep(3)
