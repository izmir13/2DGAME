import random
import json
import os

from pico2d import *
from math import *

import game_framework
import title_state

name = "MainState"

background = None
team1 = None
team2 = None
bullet = list()
block = list()
font = None

class BackGround:
    Image = None
    def __init__(self):
        self.x = 600
        self.y = 300
        if BackGround.Image == None:
            BackGround.Image = load_image('Backgroung.png')
    def draw(self):
        self.Image.draw(self.x,self.y)

class Block:
    Image = None
    def __init__(self, x, y, type):
        if Block.Image == None:
            Block.Image = load_image('Block.png')
        self.x = x
        self.y = y
        self.type = type
        self.strength = 3
    def draw(self):
        self.Image.clip_draw((self.strength - 3) * 45,self.type * 45,45,45,self.x,self.y)

class Bullet:
    Image = None
    def __init__(self,x,y,power,angle):
        self.x = x                      #초기위치
        self.y = y                      #초기위치
        self.moveX = 0                  #움직인위치
        self.moveY = 0                  #움직인위치
        self.speed = power
        self.angle = angle
        self.v_x = power * cos(angle)   #x축속도
        self.v_y = power * cos(angle)   #y축속도
        self.time = 0.1                 #시간
        if Bullet.Image == None:
            Bullet.Image = load_image('Bullet1.png')
        self.frame = 0
    def update(self):
        self.time += 0.2
        self.frame = (self.frame + 1) % 4
        self.moveX = self.x + (self.speed * sin(pi * self.angle / 180)) * self.time
        self.moveY = self.y + (self.speed * cos(pi * self.angle / 180)) * self.time + 0.5 * (-0.98) * self.time * self.time
    def draw(self):
        self.Image.clip_draw(self.frame * 12,0,12,12,self.moveX,self.moveY)


class Soldier:
    Team1_RightImage = None
    Team1_LeftImage = None
    Team2_RightImage = None
    Team2_LeftImage = None
    Aim_Image = None
    team1_turn = 0
    team2_turn = 0
    GAME_TURN = 1
    BOY_MOVE, BOY_AIM = 0,1

    def handle_boy_move(self):
        #움직일때 애니메이션
        self.frame = (self.frame + 1) % self.CharacterFrame

        if self.moveRight:
            self.x += 1
        if self.moveLeft:
            self.x -= 1

    def handle_boy_aim(self):
        #조준일때 애니메이션
        temp = 0        
        if self.angle <= 0:     #각도를 양수로 초기화.
            temp = -self.angle
        else:
            temp = self.angle
        if temp <= 22.5:
            self.frame = 7
        elif temp > 22.5 and temp <= 45:
            self.frame = 6
        elif temp > 45 and temp <= 67.5:
            self.frame = 5
        elif temp > 67.5 and temp <= 90:
            self.frame = 4
        elif temp > 90 and temp <= 112.5:
            self.frame = 3
        elif temp > 112.5 and temp <= 135:
            self.frame = 2
        elif temp > 135 and temp <= 157.5:
            self.frame = 1
        elif temp > 157.5:
                self.frame = 0
        
        if self.angle <= -180:
            self.angle = -180
        if self.angle >= 180:
            self.angle = 180
        if self.DrawImage == False:     # -180 ~ 0 일때 (왼쪽)
            if self.angle >= 0:
                self.angle *= -1
        if self.DrawImage == True:
            if self.angle <= 0:
                self.angle *= -1

        if self.increAngel:
            self.angle += 1
        if self.decreAngel:
            self.angle -= 1
        if self.charge:
            self.power += 0.2

    handle_state = {
                BOY_MOVE: handle_boy_move,
                BOY_AIM: handle_boy_aim
    }

    def __init__(self,team):
        self.x = random.randint(200,1000)
        self.y = random.randint(200,400)
        if team == 1:                                          # team1
            if Soldier.Team1_RightImage == None:
                Soldier.Team1_RightImage = load_image('ModernArmy_R_1.png')
            if Soldier.Team1_LeftImage == None:
                Soldier.Team1_LeftImage = load_image('ModernArmy_L_1.png')
        if team == 2:                                          # team2
            if Soldier.Team2_RightImage == None:
                Soldier.Team2_RightImage = load_image('ModernArmy_R_2.png')
            if Soldier.Team2_LeftImage == None:
                Soldier.Team2_LeftImage = load_image('ModernArmy_L_2.png')
        if Soldier.Aim_Image == None:
            Soldier.Aim = load_image('Bullet1.png')
        self.DrawImage = random.randint(0,1)
        self.state = State.Idle
        self.BOY_STATE = self.BOY_MOVE
        self.moveRight = False
        self.moveLeft = False
        self.CharacterFrame = Frame.Idle
        self.frame = random.randint(0,5)
        self.angle = -90
        self.increAngel = False
        self.decreAngel = False
        self.power = 0.0
        self.charge = False
        self.team = team

    def update(self):
        self.handle_state[self.BOY_STATE](self)
        

    def draw(self):
        if self.team == 1:
            if self.DrawImage:
                self.Team1_RightImage.clip_draw(self.frame * 60, self.state, 60, 80, self.x, self.y)
            else:
                self.Team1_LeftImage.clip_draw(self.frame * 60, self.state, 60, 80, self.x, self.y)
        elif self.team == 2:
            if self.DrawImage:
                self.Team2_RightImage.clip_draw(self.frame * 60, self.state, 60, 80, self.x, self.y)
            else:
                self.Team2_LeftImage.clip_draw(self.frame * 60, self.state, 60, 80, self.x, self.y)

        if self.BOY_STATE == self.BOY_AIM:
            self.Aim.clip_draw(36,0,12,12,self.x + 50 * sin(pi * self.angle / 180),self.y + 50 * cos(pi * self.angle / 180))


    def boyevent(self,event):
        if event.type == SDL_KEYDOWN:   #키가 눌렸을때
            if event.key == SDLK_RIGHT:                             #   →
                self.DrawImage = True
                self.moveRight = True
                self.CharacterFrame = Frame.Move
                self.state = State.Move
                self.BOY_STATE = self.BOY_MOVE
            if event.key == SDLK_LEFT:                              #   ←
                self.DrawImage = False
                self.moveLeft = True
                self.CharacterFrame = Frame.Move
                self.state = State.Move
                self.BOY_STATE = self.BOY_MOVE
            if event.key == SDLK_UP:                                #   ↑
                self.CharacterFrame = Frame.Aim
                self.state = State.Aim
                self.BOY_STATE = self.BOY_AIM
                if self.DrawImage == True:
                    self.decreAngel = True
                if self.DrawImage == False:
                    self.increAngel = True
            if event.key == SDLK_DOWN:                              #   ↓
                self.CharacterFrame = Frame.Aim
                self.state = State.Aim
                self.BOY_STATE = self.BOY_AIM
                if self.DrawImage == True:
                    self.increAngel = True
                if self.DrawImage == False:
                    self.decreAngel = True
            if event.key == SDLK_SPACE and self.state == State.Aim:
                self.charge = True

        if event.type == SDL_KEYUP:     #키를 땠을때
            if event.key == SDLK_RIGHT:                             #   →
                self.DrawImage = True
                self.moveRight = False
                self.CharacterFrame = Frame.Idle
                self.state = State.Idle
                self.BOY_STATE = self.BOY_MOVE
                self.frame = 0                                               
            if event.key == SDLK_LEFT:                              #   ←
                self.DrawImage = False
                self.moveLeft = False
                self.CharacterFrame = Frame.Idle
                self.state = State.Idle
                self.BOY_STATE = self.BOY_MOVE                                      
                self.frame = 0
            if (event.key == SDLK_UP) or (event.key == SDLK_DOWN):  #   ↑  ↓
                self.frame = 0
                self.increAngel = False
                self.decreAngel = False
            if event.key == SDLK_SPACE and self.state == State.Aim:
                self.charge = False                                          
                bullet.append(Bullet(self.x,self.y,self.power,self.angle))
                self.power = 0
                self.CharacterFrame = Frame.Idle
                self.state = State.Idle
                self.BOY_STATE = self.BOY_MOVE
                self.moveRight = False
                self.moveLeft = False
                if self.team == 1:
                    Soldier.team1_turn = (Soldier.team1_turn + 1) % 3
                    Soldier.GAME_TURN = 2
                elif self.team == 2:
                    Soldier.team2_turn = (Soldier.team2_turn + 1) % 3
                    Soldier.GAME_TURN = 1

def MakeMap():
    global block
    f = open('map.txt','r')
    s = f.read()
    l = s.split()
    count = 0
    for i in l:
        if (int)(i) != 0:
            block.append(Block((count % 26)* 45 + 22,(int)(count / 26)* 45 + 22,(int)(i)-1))
        count += 1
    f.close()

def enter():
    MakeMap()
    global background
    background = BackGround()
    global team1
    team1 = [Soldier(1) for i in range(3)]
    global team2
    team2 = [Soldier(2) for i in range(3)]

def exit():
    global background
    del(background)
    global team1
    del(team1)
    global team2
    del(team2)
    global bullet
    del(bullet)

def pause():
    pass

def resume():
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        if Soldier.GAME_TURN == 1:
            team1[Soldier.team1_turn].boyevent(event)
        elif Soldier.GAME_TURN == 2:
            team2[Soldier.team2_turn].boyevent(event)

def update():
    for i in team1:
        i.update()
    for i in team2:
        i.update()
    for i in bullet:
        i.update()

def draw():
    clear_canvas()
    background.draw()
    for i in block:
        i.draw()
    for i in team1:
        i.draw()
    for i in team2:
        i.draw()
    for i in bullet:
        i.draw()
    update_canvas()
    delay(0.01)






class State:
    Idle = 320
    Move = 240
    Jump = 160
    Aim = 80
    Shoot = 0

class Frame:
    Idle = 5
    Move = 6
    Jump = 5
    Aim = 8
    Shoot = 8
