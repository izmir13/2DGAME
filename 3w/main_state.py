import random
import json
import os

from pico2d import *
from math import *

import game_framework
import title_state

name = "MainState"

boy = None
bullet = list()
font = None

class Bullet:
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
        self.Image = load_image('Bullet1.png')
        self.frame = 0
    def update(self):
        self.time += 0.2
        self.frame = (self.frame + 1) % 4
        self.moveX = self.x + (self.speed * sin(pi * self.angle / 180)) * self.time
        self.moveY = self.y + (self.speed * cos(pi * self.angle / 180)) * self.time + 0.5 * (-0.98) * self.time * self.time
    def draw(self):
        self.Image.clip_draw(self.frame * 12,0,12,12,self.moveX,self.moveY)

class Boy:
    def __init__(self):
        self.x = random.randint(200,1000)
        self.y = random.randint(200,400)
        self.RightImage = load_image('ModernArmy_R.png')
        self.LeftImage = load_image('ModernArmy_L.png')
        self.Aim = load_image('Bullet1.png')
        self.DrawImage = False
        self.state = State.Idle
        self.moveRight = False
        self.moveLeft = False
        self.CharacterFrame = Frame.Idle
        self.frame = 0
        self.angle = -180
        self.increAngel = False
        self.decreAngel = False
        self.power = 0.0
        self.charge = False

    def update(self):
        if (self.CharacterFrame != Frame.Aim) or (self.CharacterFrame != Frame.Shoot):
            self.frame = (self.frame + 1) % self.CharacterFrame
        else:
            temp = 0
            if self.angle <= 0:
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

        if self.moveRight:
            self.x += 1
        if self.moveLeft:
            self.x -= 1
        if self.increAngel:
            self.angle += 1
        if self.decreAngel:
            self.angle -= 1
        if self.charge:
            self.power += 0.2

        #Aim 조준...
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

    def draw(self):
        if self.DrawImage:
            self.RightImage.clip_draw(self.frame * 60, self.state, 60, 80, self.x, self.y)
        else:
            self.LeftImage.clip_draw(self.frame * 60, self.state, 60, 80, self.x, self.y)
        self.Aim.clip_draw(36,0,12,12,self.x + 50 * sin(pi * self.angle / 180),self.y + 50 * cos(pi * self.angle / 180))

    def boyevent(self,event):
        if event.type == SDL_KEYDOWN:   #키가 눌렸을때
            if event.key == SDLK_RIGHT:
                self.DrawImage = True
                self.moveRight = True
                self.CharacterFrame = Frame.Move
                self.state = State.Move
            if event.key == SDLK_LEFT:
                self.DrawImage = False
                self.moveLeft = True
                self.CharacterFrame = Frame.Move
                self.state = State.Move
            if event.key == SDLK_UP:
                self.CharacterFrame = Frame.Aim
                self.state = State.Aim
                if self.DrawImage == True:
                    self.decreAngel = True
                if self.DrawImage == False:
                    self.increAngel = True
            if event.key == SDLK_DOWN:
                self.CharacterFrame = Frame.Aim
                self.state = State.Aim
                if self.DrawImage == True:
                    self.increAngel = True
                if self.DrawImage == False:
                    self.decreAngel = True
            if event.key == SDLK_SPACE and self.state == State.Aim:
                self.charge = True

        if event.type == SDL_KEYUP:     #키를 땠을때
            if event.key == SDLK_RIGHT:
                self.DrawImage = True
                self.moveRight = False
                self.CharacterFrame = Frame.Idle
                self.state = State.Idle
                self.frame = 0
            if event.key == SDLK_LEFT:
                self.DrawImage = False
                self.moveLeft = False
                self.CharacterFrame = Frame.Idle
                self.state = State.Idle
                self.frame = 0
            if (event.key == SDLK_UP) or (event.key == SDLK_DOWN):
                self.frame = 0
                self.increAngel = False
                self.decreAngel = False
            if event.key == SDLK_SPACE and self.state == State.Aim:
                self.charge = False
                bullet.append(Bullet(self.x,self.y,self.power,self.angle))
                self.power = 0
                

def enter():
    global boy
    boy = Boy()

def exit():
    global boy
    del(boy)

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
        boy.boyevent(event)

def update():
    boy.update()
    for i in bullet:
        i.update()

def draw():
    clear_canvas()
    boy.draw()
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
