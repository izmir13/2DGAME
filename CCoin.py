﻿from pico2d import *
from math import *
import random

class Coin:
    Image = None
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 9
    def __init__(self,x,y,power,angle):  
        self.x = x                      #초기위치
        self.y = y                      #초기위치
        self.moveX = 0                  #움직인위치
        self.moveY = 0                  #움직인위치
        self.speed = power
        self.angle = angle
        self.time = 0.1                 #시간
        if Coin.Image == None:
            Coin.Image = load_image('image//coin.png')
        self.total_frames = 0
        self.frame = 0
    def update(self,frame_time,wind,scroll_x,scroll_y):
        self.time += 20 * frame_time
        self.total_frames += Coin.FRAMES_PER_ACTION * Coin.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 9
        self.moveX = self.x + ((self.speed * sin(pi * self.angle / 180)) * self.time + 0.5 * (wind) * self.time)
        self.moveY = self.y + ((self.speed * cos(pi * self.angle / 180)) * self.time + 0.5 * (-9.8) * self.time)
        #print(scroll_x,"\t",scroll_y)
        if self.moveY < -scroll_y-100:
            self.x = random.randint(int(-scroll_x),int(1200-scroll_x))                      #초기위치
            self.y = random.randint(int(600-scroll_y),int(700-scroll_y))                     #초기위치
            #self.moveX = 0                  #움직인위치
            #self.moveY = 0                  #움직인위치
            self.time = 0.1 
        if self.moveX > 1200-scroll_x:
            self.x = -scroll_x
            self.y = self.moveY
            #self.moveX = 0                  #움직인위치
            #self.moveY = 0                  #움직인위치
            self.time = 0.1 
        if self.moveX < -scroll_x:
            self.x = 1200-scroll_x
            self.y = self.moveY
            #self.moveX = 0                  #움직인위치
            #self.moveY = 0                  #움직인위치
            self.time = 0.1 

    def draw(self,scroll_x,scroll_y):
        self.Image.clip_draw(self.frame * 14,0,14,14,self.moveX + scroll_x,self.moveY + scroll_y)