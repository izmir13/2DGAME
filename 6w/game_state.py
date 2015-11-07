from pico2d import *
import game_framework
import title_state
import random

from enum import *
from CBlock import *
from CSoldier import *
from CBullet import *
from CCoin import *
from collision import *
from CUI import *

name = "GameState"

squad_num = 2
wind = 0

background = None
ui = None
block = list()
team_green = None
team_gray = None
play_turn = 0
bullet = list()
coin = list()

class BackGround:
    Image = None
    def __init__(self):
        self.x = 600
        self.y = 300
        if BackGround.Image == None:
            BackGround.Image = load_image('image//Backgroung.png')
    def draw(self):
        self.Image.draw(self.x,self.y)

def makemap():
    global block
    f = open('map.txt','r')
    s = f.read()
    l = s.split()
    count = 0
    for i in l:
        if (int)(i) != 0:
            block.append(Block((count % 27)* 45 + 22,(int)(count / 27)* 45 + 22,(int)(i)-1))
        count += 1
    f.close()


def enter():
    makemap()
    global background
    background = BackGround()
    global ui
    ui = CUI()
    global team_green
    team_green = [Soldier(SoldierTeam.Green) for i in range(squad_num)]
    global team_gray
    team_gray = [Soldier(SoldierTeam.Gray) for i in range(squad_num)]
    global coin
    for i in range(30):
        coin.append(Coin(random.randint(0,1200),random.randint(0,600),0,0))

def exit():
    global block
    del(block)
    global background
    del(background)
    global ui
    del(ui)
    global team_green
    del(team_green)
    global team_gray
    del(team_gray)
    global bullet
    del(bullet)
    global coin
    del(coin)

def pause():
    pass

def resume():
    pass

def handle_events():
    #global play_turn
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        #elif event.type == SDL_KEYUP and event.key == SDLK_ESCAPE:
        #    game_framework.change_state(title_state)
        elif len(bullet) == 0:
            if (play_turn % 2) == SoldierTeam.Green:
                team_green[int(play_turn/2)].event(event,bullet,wind)
            elif (play_turn % 2) == SoldierTeam.Gray:
                team_gray[int(play_turn/2)].event(event,bullet,wind)

def update():
    global play_turn
    global wind
    global block
    #for i in block:
    #    for j in team_green:
    #        collision_Soldier_and_Block(j,i)
    #    for k in team_gray:
    #        collision_Soldier_and_Block(k,i)

    for i in block:
        for j in team_green:
            collision_soldier_and_block(j,i)
        for k in team_gray:
            collision_soldier_and_block(k,i)

    for i in coin:
        i.update(wind)
    for i in bullet:
        i.update()
        print(i.moveY)
        if i.moveY < 0:
            bullet.clear()
            play_turn = (play_turn + 1) % (squad_num*2)
            wind = random.randint(-10,10)
    for i in team_green:
        i.update()
    for i in team_gray:
        i.update()

def draw():
    clear_canvas()
    background.draw()
    for i in coin:
        i.draw()
    for i in block:
        i.draw()
        i.draw_bb()
    for i in bullet:
        i.draw()
    for i in team_green:
        i.draw()
        i.draw_bb()
    for i in team_gray:
        i.draw()
        i.draw_bb()

    if (play_turn % 2) == SoldierTeam.Green:
        ui.draw(int(team_green[int(play_turn/2)].get_power()))
    elif (play_turn % 2) == SoldierTeam.Gray:
        ui.draw(int(team_gray[int(play_turn/2)].get_power()))

    update_canvas()