import os
import random
import curses
import numpy as np

"""
Additional files needed to run properly:
    "HIGHSCORE.txt"
    "spaceinvaders.mp3"
    
By: Joe Ulseth
Date: 8/30/2020
(P.S. I've never made a game before, so relax if this is shit and hacked together)
    
"""


# LOADING SCREEN
def loading_screen(BONUS, mode = 'initalize'):
    with open("HIGHSCORE.txt", "r") as f:
        line = f.readline()
        if line == '':
            old_highscore = 0
            highscore_to_screen = "OLD HIGH SCORE:  0"
        else:
            old_highscore = int(line)
            highscore_to_screen = "OLD HIGH SCORE:  "+line
            
    if mode == 'initalize':
        w.addstr(int(SH/2)-4, int(0.45*SW), "PLAY PYTHON SPACE INVADERS")
        w.addstr(int(SH/2)-2, int(0.45*SW), "QUIT")
        w.addstr(int(SH/2), int(0.45*SW), highscore_to_screen)
        w.addstr(int(SH/2)-4, int(0.4*SW), "--->")
        CHOICE = "top"
        LOADING = True
        while LOADING == True:
            next_key = w.getch()
            key = 0 if next_key == -1 else next_key
            if (key == curses.KEY_DOWN) and (CHOICE == "top"):
                w.addstr(int(SH/2)-4, int(0.4*SW), "    ")
                w.addstr(int(SH/2)-2, int(0.4*SW), "--->")
                CHOICE = "bottom"
            if (key == curses.KEY_UP) and (CHOICE == "bottom"):
                w.addstr(int(SH/2)-2, int(0.4*SW), "    ")
                w.addstr(int(SH/2)-4, int(0.4*SW), "--->")
                CHOICE = "top"
            if (key == 10) and (CHOICE == "top"):
                w.erase()
                LOADING = False
                return 0
            if (key == 10) and (CHOICE == "bottom"):
                PID = os.system("pidof watch")
                os.system("kill "+str(PID))
                curses.endwin()
                quit()

                
    if mode == 'retry':
        w.addstr(int(SH/2)-4, int(0.45*SW), "PLAY PYTHON SPACE INVADERS")
        w.addstr(int(SH/2)-2, int(0.45*SW), "QUIT")
        w.addstr(int(SH/2), int(0.5*SW), "You hit a rock! :(")
        w.addstr(int(SH/2)+1, int(0.5*SW), "YOUR SCORE:    "+str(BONUS))
        if old_highscore < BONUS:
            with open("HIGHSCORE.txt", "w") as f:
                f.write(str(BONUS))
            w.addstr(int(SH/2)+2, int(0.5*SW), "~ ~ ~ NEW HIGH SCORE! ~ ~ ~" )
            
        w.addstr(int(SH/2)+4, int(0.45*SW), highscore_to_screen)
        w.addstr(int(SH/2)-4, int(0.4*SW), "--->")
        CHOICE = "top"
        LOADING = True
        while LOADING == True:
            next_key = w.getch()
            key = 0 if next_key == -1 else next_key
            if (key == curses.KEY_DOWN) and (CHOICE == "top"):
                w.addstr(int(SH/2)-4, int(0.4*SW), "    ")
                w.addstr(int(SH/2)-2, int(0.4*SW), "--->")
                CHOICE = "bottom"
            if (key == curses.KEY_UP) and (CHOICE == "bottom"):
                w.addstr(int(SH/2)-2, int(0.4*SW), "    ")
                w.addstr(int(SH/2)-4, int(0.4*SW), "--->")
                CHOICE = "top"
            if (key == 10) and (CHOICE == "top"):
                w.erase()
                LOADING = False
                return 0
            if (key == 10) and (CHOICE == "bottom"):
                PID = os.system("pidof watch")
                os.system("kill "+str(PID))
                curses.endwin()
                quit()

def update_rocks(loop_count,BONUS,speed):
    delete_rocks = []
    if loop_count%10 == 0:
        new_rock = [[1,random.randint(1,SW-1)]]
        all_rocks.append(new_rock)
        w.addch(new_rock[0][0],new_rock[0][1], '▢')
    for i,r in enumerate(all_rocks):
        rx = r[0][1]
        w.addch(r[0][0], rx, ' ')
        if loop_count%10 == 0:
            r[0][0] += 1
        ry = r[0][0]
        explosion_zone = [ [ry,rx],[ry,rx-1],[ry,rx+1],[ry+1,rx],[ry+1,rx-1],[ry+1,rx+1] ]
        if (ry < SH-2):
            w.addch(ry,rx,'▢') 
        else:
            delete_rocks.append(i)
        if any(item in explosion_zone for [item] in fired_bullets):
            debris = [ [ry,rx],[ry-1,rx],[ry+1,rx],[ry,rx-1],[ry,rx+1] ]
            if debris not in all_debris:
                all_debris.append(debris)
            w.addch(ry,rx,' ')
            w.addch(ry-1,rx,'|')
            w.addch(ry+1,rx,'|')
            w.addch(ry,rx-1,'-')
            w.addch(ry,rx+1,'-')
            w.addch(ry,rx,'*')
            BONUS += 25
            if i not in delete_rocks:
                delete_rocks.append(i)
    
    if (loop_count%2000 == 0) and (loop_count != 0) and (loop_count < 8000) and (speed >= 4):
        w.erase()
        speed -= 2
        w.timeout(speed)
        return delete_rocks, [], BONUS, speed
    else:
        return delete_rocks, all_rocks, BONUS, speed

def update_bullets_pack(loop_count,speed):
    delete_bullets_pack = []
    if loop_count%100 == 0:
        new_bullets = [[1,random.randint(1,SW-1)]]
        all_bullets_pack.append(new_bullets)
        w.addstr(new_bullets[0][0], new_bullets[0][1], '|+++|')
    for i,bp in enumerate(all_bullets_pack):
        w.addstr(bp[0][0], bp[0][1], '     ')
        if loop_count%10 == 0:
            bp[0][0] += 1
        if bp[0][0] < SH-2:
            w.addstr(bp[0][0],bp[0][1],'|+++|')
        else: 
            delete_bullets_pack.append(i)
                
    if (loop_count%2000 == 0) and (loop_count != 0) and (loop_count < 8000) and (speed >= 4):
        w.erase()
        return delete_bullets_pack, []
    else:
        return delete_bullets_pack, all_bullets_pack
        
def update_bullets_fired(loop_count,speed):
    delete_bullets_fired = []
    for i,fb in enumerate(fired_bullets):
        w.addch(fb[0][0], fb[0][1], ' ')
        if loop_count%10 == 0:
            fb[0][0] -= 1
        if fb[0][0] > 3:
            w.addch(fb[0][0], fb[0][1], '|')
        else:
            delete_bullets_fired.append(i)
                
    return delete_bullets_fired, fired_bullets

def clear_screen():
    for i in range(len(all_rocks)):
        if i in delete_rocks:
            all_rocks.pop(i)
            
    for i in range(len(all_bullets_pack)):
        if i in delete_bullets_pack:
            all_bullets_pack.pop(i)
    
    for i in range(len(fired_bullets)):
        if i in delete_bullets_fired:
            try:
                fired_bullets.pop(i)  
            except:
                PID = os.system("pidof watch")
                os.system("kill "+str(PID))
                os.system('echo "ERROR deleting fired bullets" ') # sometimes this happens...
            
            
            
def clear_debris(loop_count):
    if loop_count%20 == 0:
        for i,debris_clump in enumerate(all_debris):
            for piece in range(5):
                w.addch(debris_clump[piece][0], debris_clump[piece][1],' ')
        return []
    else:
        return all_debris

    
        
# INITIALIZE SCREEN
os.system("watch -n 1 nohup mpg123 -q "+"spaceinvaders.mp3 &") #play song on repeat, and in quiet mode (-q) so no text is output to screen
speed = 15
s = curses.initscr()
curses.curs_set(0)
SH, SW = s.getmaxyx() #Screen Height, Screen Width
w = curses.newwin(SH, SW, 0, 0)
w.keypad(1)
w.timeout(speed)
        
spaceship_x = int(SW/2) # put ship centered horizontally to begin
spaceship_y = SH-2 # put ship near the bottom
spaceship_head = [ [spaceship_y,spaceship_x] ]
spaceship = [ [spaceship_y+1, spaceship_x-1] ]

all_rocks = []
all_bullets_pack = []
fired_bullets = []
all_debris = []
loop_count = 0
num_bullets = 20
BONUS = 0

loop_count = loading_screen(loop_count)
while True:
    next_key = w.getch()
    key = 0 if next_key == -1 else next_key
    
    # ADD ROCKS, BULLET PACKAGES, AND FIRED BULLETS
    delete_rocks, all_rocks, BONUS, speed = update_rocks(loop_count,BONUS,speed)
    delete_bullets_pack, all_bullets_pack = update_bullets_pack(loop_count,speed)
    delete_bullets_fired, fired_bullets = update_bullets_fired(loop_count,speed)
   
    h = [spaceship_head[0][0], spaceship_head[0][1]] # h = head of spaceship (gun)
    b = [spaceship[0][0], spaceship[0][1]]
        
    spaceship_head.insert(0,h)
    spaceship.insert(0,b)
    
    if key == curses.KEY_LEFT:
        h[1] -= 1
        b[1] -= 1
    if key == curses.KEY_RIGHT:
        h[1] += 1
        b[1] += 1
    if key == curses.KEY_UP:
        if num_bullets > 0:
            num_bullets -= 1
            fired_bullet = [ [h[0]-1,h[1] ] ]
            fired_bullets.append(fired_bullet)
            w.addch(h[0],h[1], '|')
    
    ship_zone = [ [[h[0],h[1]-2]],[[h[0],h[1]-1]],[[h[0],h[1]]],[[h[0],h[1]+1]],[[h[0],h[1]+2]] ]
    if any(item in ship_zone for item in all_bullets_pack) :
        num_bullets += 10
    if any(item in ship_zone for item in all_rocks):
        all_rocks = []
        all_bullets_pack = []
        fired_bullets = []
        num_bullets = 20
        speed = 15
        loop_count = 0
        BONUS = loading_screen(BONUS, mode = 'retry')
        h[1] = spaceship_x
        b[1] = spaceship_x-1
        
    else:
        move_h = spaceship_head.pop()
        move_b = spaceship.pop()
        w.addch(move_h[0], move_h[1], ' ')
        w.addstr(move_b[0], move_b[1], '   ')
        
    
    all_debris = clear_debris(loop_count)
    clear_screen()
            
    loop_count += 1
    score = 'Score: '+str(BONUS)
    bullets_score = 'Bullets: '+str(num_bullets)
    w.addch(spaceship_head[0][0], spaceship_head[0][1], '|')
    w.addstr(spaceship[0][0], spaceship[0][1], '/+\\')
    w.addstr(SH-1,2,'             ')
    w.addstr(SH-1,2,score)
    w.addstr(SH-1,15,'               ')
    w.addstr(SH-1,15,bullets_score)  #glitchy when song restarts due to clearing the screen
    
