from pico2d import *
from math import *
import random

class Coin:
    Image = None
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
        self.frame = 0
    def update(self,wind):
        self.time += 0.1
        self.frame = (self.frame + 1) % 9
        self.moveX = self.x + (self.speed * sin(pi * self.angle / 180)) * self.time + 0.5 * (wind / 2.0) * self.time
        self.moveY = self.y + (self.speed * cos(pi * self.angle / 180)) * self.time + 0.5 * (-9.8) * self.time
        if self.moveY < 0:
            self.x = random.randint(0,1200)                      #초기위치
            self.y = random.randint(600,700)                     #초기위치
            self.moveX = 0                  #움직인위치
            self.moveY = 0                  #움직인위치
            self.time = 0.1 
        if self.moveX > 1200:
            self.x = 0
            self.y = self.moveY
            self.moveX = 0                  #움직인위치
            self.moveY = 0                  #움직인위치
            self.time = 0.1 
        if self.moveX < 0:
            self.x = 1200
            self.y = self.moveY
            self.moveX = 0                  #움직인위치
            self.moveY = 0                  #움직인위치
            self.time = 0.1 

    def draw(self):
        self.Image.clip_draw(self.frame * 14,0,14,14,self.moveX,self.moveY)