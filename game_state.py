from pico2d import *
import game_framework
import title_state
import random
import time

from myenum import *
from CBlock import *
from CSoldier import *
from CBullet import *
from CCoin import *
from collision import *
from CUI import *
from CAnimation import *
from CItem import *
from CMenu import *
name = "GameState"

move_speed = 0
play_x = 0
play_y = 0
scroll_x = 0
scroll_y = 0
left_move = False
right_move = False
top_move = False
bottom_move = False
squad_num = None
#squad_num = 5       #팀원 수
map_num = None
wind = wind = random.randint(1,3)

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
pos = list()
play_time = 0

class BackGround:
    Image = None
    def __init__(self):
        self.x = 600
        self.y = 300
        if BackGround.Image == None:
            BackGround.Image = load_image('image//Backgroung.png')
    def draw(self):
        self.Image.draw(self.x,self.y)

class Pos:
    def __init__(self,x,y):
        self.x = x
        self.y = y

def makemap():
    global map_num
    global block
    global pos
    if map_num == 1:
        f = open('map1.txt','r')
    if map_num == 2:
        f = open('map2.txt','r')
    s = f.read()
    l = s.split()
    count = 0
    for i in l:
        if (int)(i) != 0 and (int)(i) != 8:
            block.append(Block((count % 54)* 45 + 22,(int)(count / 54)* 45 + 22,(int)(i)-1))
        if (int)(i) == 8:
            pos.append(Pos((count % 54)* 45 + 22,(int)(count / 54)* 45 + 22))
        count += 1
    f.close()

def enter():
    global squad_num
    global font
    global play_time
    font = load_font('kenvector_future.TTF')                         #폰트..
    makemap()
    global background
    background = BackGround()
    global ui
    ui = CUI()
    global team_green
    team_green = [Soldier(SoldierTeam.Green,pos) for i in range(squad_num)]
    global team_gray
    team_gray = [Soldier(SoldierTeam.Gray,pos) for i in range(squad_num)]
    global coin
    for i in range(30):
        coin.append(Coin(random.randint(0,1200),random.randint(0,600),0,0))
    play_time = time.clock()

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
    global move_speed
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
            move_speed = 0
        elif event.type == SDL_KEYUP and event.key == SDLK_d:
            right_move = False
            move_speed = 0
        elif event.type == SDL_KEYDOWN and event.key == SDLK_w:
            top_move = True
        elif event.type == SDL_KEYDOWN and event.key == SDLK_s:
            bottom_move = True
        elif event.type == SDL_KEYUP and event.key == SDLK_w:
            top_move = False
            move_speed = 0
        elif event.type == SDL_KEYUP and event.key == SDLK_s:
            bottom_move = False
            move_speed = 0
        elif len(bullet) == 0:
            if Player_turn == SoldierTeam.Green and len(team_green):
                team_green[0].event(event,bullet,wind)
            elif Player_turn == SoldierTeam.Gray and len(team_gray):
                team_gray[0].event(event,bullet,wind)

def move_screen(play_x,play_y,scroll_x,scroll_y,frame_time):
    global move_speed
    #print(move_speed)
    if (play_x + scroll_x <= 300 or play_x + scroll_x >= 900) or (play_y + scroll_y <= 200 or play_y + scroll_y >= 400):
        move_speed += 500 * frame_time
    else:
        move_speed = 0

    if play_x + scroll_x <= 300:
        scroll_x += (150 + move_speed) * frame_time
    elif play_x + scroll_x >= 900:
        scroll_x -= (150 + move_speed) * frame_time
    if play_y + scroll_y <= 200:
        scroll_y += (150 + move_speed) * frame_time
    elif play_y + scroll_y >= 400:
        scroll_y -= (150 + move_speed) * frame_time

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
    global play_time
    total_hp_green = 0
    total_hp_gray = 0
    #print(play_x,"\t",play_y)

    if left_move:
        scroll_x += (600 + move_speed) * frame_time
    if right_move:
        scroll_x -= (600 + move_speed) * frame_time
    if top_move:
        scroll_y -= (600 + move_speed) * frame_time
    if bottom_move:
        scroll_y += (600 + move_speed) * frame_time

    if len(bullet) <= 0 and int(time.clock() - play_time) >= 15:
        play_time = time.clock()
        if Player_turn == SoldierTeam.Green:
            Player_turn = SoldierTeam.Gray
            if len(team_green):
                team_green[0].moveRight = False
                team_green[0].moveLeft = False
                team_green[0].state = SoldierState.Idle
                team_green[0].STATE = SoldierHandle.IDLE
                team_green[0].characterframe = SoldierFrame.Idle
                team_green[0].frame = 0     
                team_green[0].increAngel = False
                team_green[0].decreAngel = False
                team_green[0].charge = False
                team_green[0].power = 0
                team_green.insert(0,team_green.pop())
                                    
        elif Player_turn == SoldierTeam.Gray:
            Player_turn = SoldierTeam.Green
            if len(team_gray):
                team_gray[0].moveRight = False
                team_gray[0].moveLeft = False
                team_gray[0].state = SoldierState.Idle
                team_gray[0].STATE = SoldierHandle.IDLE
                team_gray[0].characterframe = SoldierFrame.Idle
                team_gray[0].frame = 0     
                team_gray[0].increAngel = False
                team_gray[0].decreAngel = False
                team_gray[0].charge = False
                team_gray[0].power = 0
                team_gray.insert(0,team_gray.pop())

    #print(int(time.clock() - play_time))

    turn = collision_bullet_and_obj(bullet,block,team_green,team_gray,item,animation)
    if turn:
        if len(bullet) <= 0 and Player_turn == SoldierTeam.Green:
            Player_turn = SoldierTeam.Gray
            if len(team_green):
                team_green.insert(0,team_green.pop())
                create_item += 1
                play_time = time.clock()
        elif len(bullet) <= 0 and Player_turn == SoldierTeam.Gray:
            Player_turn = SoldierTeam.Green
            if len(team_gray):
                team_gray.insert(0,team_gray.pop())
                create_item += 1
                play_time = time.clock()

        wind = random.randint(-10,10)
        while wind == 0:
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
        i.update(frame_time,wind,scroll_x,scroll_y)
    for i in bullet:
        i.update(frame_time)
        if i.y < -100:
            bullet.clear()
            if Player_turn == SoldierTeam.Green:
                Player_turn = SoldierTeam.Gray
                play_time = time.clock()
                team_green.insert(0,team_green.pop())
            else:
                Player_turn = SoldierTeam.Green
                play_time = time.clock()
                team_gray.insert(0,team_gray.pop())
            wind = random.randint(-10,10)
    for i in item:
        i.update(frame_time)
    for i in team_green:
        total_hp_green += i.get_hp()
        item_type = collision_soldier_and_item(i,item)
        i.update(frame_time,item_type)
        if i.y < -100:
            Player_turn = SoldierTeam.Gray
            team_green.remove(i)
    for i in team_gray:
        total_hp_gray += i.get_hp()
        item_type = collision_soldier_and_item(i,item)
        i.update(frame_time,item_type)
        if i.y < -100:
            Player_turn = SoldierTeam.Green
            team_gray.remove(i)
    for i in animation:
        i.update(frame_time)
        if i.frame >= 25:
            animation.remove(i)
    ui.update(frame_time,wind,int(time.clock() - play_time),total_hp_green,total_hp_gray,squad_num)
    

def draw(frame_time):
    clear_canvas()
    background.draw()
    power = 0
    p_x = 0
    p_y = 0

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
        power = team_green[0].get_power()
        p_x = team_green[0].x
        p_y = team_green[0].y
        
    elif Player_turn == SoldierTeam.Gray and len(team_gray):
        power = team_gray[0].get_power()
        p_x = team_gray[0].x
        p_y = team_gray[0].y
    ui.draw(int(power),frame_time,p_x + scroll_x,p_y + scroll_y + 30)
    if wind < 0:
        font.draw(55, 85, '%d' % wind)
    else:
        font.draw(65, 85, '%d' % wind)

    #if Player_turn == SoldierTeam.Green and len(team_green):
    #    ui.draw(int(team_green[0].get_power()),frame_time,team_green[0].x + scroll_x,team_green[0].y + scroll_y + 30)
    #    if wind < 0:
    #        font.draw(55, 85, '%d' % wind)
    #    else:
    #        font.draw(65, 85, '%d' % wind)
    #elif Player_turn == SoldierTeam.Gray and len(team_gray):
    #    ui.draw(int(team_gray[0].get_power()),frame_time,team_gray[0].x + scroll_x,team_gray[0].y + scroll_y + 30)
    #    if wind < 0:
    #        font.draw(55, 85, '%d' % wind)
    #    else:
    #        font.draw(65, 85, '%d' % wind)
    update_canvas()