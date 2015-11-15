from pico2d import *
import game_framework
import title_state
import random

from myenum import *
from CBlock import *
from CSoldier import *
from CBullet import *
from CCoin import *
from collision import *
from CUI import *
from CAnimation import *
from CItem import *

name = "GameState"

play_x = 0
play_y = 0
scroll_x = 0
scroll_y = 0
left_move = False
right_move = False
top_move = False
bottom_move = False
squad_num = 2       #팀원 수
wind = 0

font = None
background = None
ui = None
block = list()
team_green = None
team_gray = None
Player_turn = SoldierTeam.Green
bullet = list()
coin = list()
animation = list()
item = list()
create_item = 0

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
    global font
    font = load_font('ENCR10B.TTF')                         #폰트..
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
    global font
    del(font)
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
    global animation
    del(animation)
    global item
    del(item)

def pause():
    pass

def resume():
    pass

def handle_events(frame_time):
    events = get_events()
    global left_move
    global right_move
    global top_move
    global bottom_move
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
            left_move = True
        elif event.type == SDL_KEYDOWN and event.key == SDLK_d:
            right_move = True
        elif event.type == SDL_KEYUP and event.key == SDLK_a:
            left_move = False
        elif event.type == SDL_KEYUP and event.key == SDLK_d:
            right_move = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_w:
            top_move = True
        elif event.type == SDL_KEYDOWN and event.key == SDLK_s:
            bottom_move = True
        elif event.type == SDL_KEYUP and event.key == SDLK_w:
            top_move = False
        elif event.type == SDL_KEYUP and event.key == SDLK_s:
            bottom_move = False
        elif len(bullet) == 0:
            if Player_turn == SoldierTeam.Green and len(team_green):
                team_green[0].event(event,bullet,wind)
            elif Player_turn == SoldierTeam.Gray and len(team_gray):
                team_gray[0].event(event,bullet,wind)

def move_screen(play_x,play_y,scroll_x,scroll_y,frame_time):
    print(scroll_y)
    if play_x + scroll_x <= 300:
        scroll_x += 400 * frame_time
    elif play_x + scroll_x >= 900:
        scroll_x -= 400 * frame_time
    if play_y + scroll_y <= 200:
        scroll_y += 400 * frame_time
    elif play_y + scroll_y >= 400:
        scroll_y -= 400 * frame_time
    return scroll_x, scroll_y

def update(frame_time):
    global play_x
    global play_y
    global create_item
    global Player_turn
    global wind
    global block
    global animation
    turn = False
    item_type = 0
    global scroll_x
    global scroll_y

    if left_move:
        scroll_x += 600 * frame_time
    if right_move:
        scroll_x -= 600 * frame_time
    if top_move:
        scroll_y -= 600 * frame_time
    if bottom_move:
        scroll_y += 600 * frame_time

    turn = collision_bullet_and_obj(bullet,block,team_green,team_gray,item,animation)
    if turn:
        if len(bullet) <= 0 and Player_turn == SoldierTeam.Green:
            Player_turn = SoldierTeam.Gray
            if len(team_green):
                team_green.insert(0,team_green.pop())
                create_item += 1
        elif len(bullet) <= 0 and Player_turn == SoldierTeam.Gray:
            Player_turn = SoldierTeam.Green
            if len(team_gray):
                team_gray.insert(0,team_gray.pop())
                create_item += 1
        wind = random.randint(-10,10)
        if create_item % 5 == 0:
            item.append(Weapon(random.randint(0,1200),600))
        if create_item % 7 == 0:
            item.append(Potion(random.randint(0,1200),600))

    if len(team_green) > 0 and len(team_gray) > 0:
        if len(bullet) <= 0 and Player_turn == SoldierTeam.Green:
            play_x = team_green[0].x
            play_y = team_green[0].y
        elif len(bullet) <= 0 and Player_turn == SoldierTeam.Gray:
            play_x = team_gray[0].x
            play_y = team_gray[0].y
        else:
            play_x = bullet[0].x
            play_y = bullet[0].y

    scroll_x, scroll_y = move_screen(play_x,play_y,scroll_x,scroll_y,frame_time) 

    for i in block:
        for j in team_green:
            collision_soldier_and_block(j,i)
        for k in team_gray:
            collision_soldier_and_block(k,i)
        for l in item:
            collision_item_and_block(l,i)

    for i in coin:
        i.update(frame_time,wind)
    for i in bullet:
        i.update(frame_time)
        if i.y < -100:
            bullet.clear()
            if Player_turn == SoldierTeam.Green:
                Player_turn = SoldierTeam.Gray
                team_green.insert(0,team_green.pop())
            else:
                Player_turn = SoldierTeam.Green
                team_gray.insert(0,team_gray.pop())
            wind = random.randint(-10,10)
    for i in item:
        i.update(frame_time)
    for i in team_green:
        item_type = collision_soldier_and_item(i,item)
        i.update(frame_time,item_type)
        if i.y < -100:
            Player_turn = SoldierTeam.Gray
            team_green.remove(i)
    for i in team_gray:
        item_type = collision_soldier_and_item(i,item)
        i.update(frame_time,item_type)
        if i.y < -100:
            Player_turn = SoldierTeam.Green
            team_gray.remove(i)
    for i in animation:
        i.update(frame_time)
        if i.frame >= 25:
            animation.remove(i)

def draw(frame_time):
    clear_canvas()
    background.draw()
    for i in coin:
        i.draw(scroll_x,scroll_y)
    for i in block:
        i.draw(scroll_x,scroll_y)
        #font.draw(i.x-10, i.y, '%d' % i.get_strength())
        #i.draw_bb()
    for i in bullet:
        i.draw(scroll_x,scroll_y)
        #i.draw_bb()
    for i in item:
        i.draw(scroll_x,scroll_y)
        #font.draw(i.x - 50, i.y +40, 'HP: %d' % i.get_hp())
        #i.draw_bb()
    for i in team_green:
        i.draw(scroll_x,scroll_y)
        #font.draw(i.x - 50, i.y +40, 'HP: %d' % i.get_hp())
        #i.draw_bb()
    for i in team_gray:
        i.draw(scroll_x,scroll_y)
        #font.draw(i.x - 50, i.y +40, 'HP: %d' % i.get_hp())
        #i.draw_bb()
    for i in animation:
        i.draw(scroll_x,scroll_y)

    if Player_turn == SoldierTeam.Green and len(team_green):
        ui.draw(int(team_green[0].get_power()))
    elif Player_turn == SoldierTeam.Gray and len(team_gray):
        ui.draw(int(team_gray[0].get_power()))

    update_canvas()