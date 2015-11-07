from pico2d import *
from math import *

class Bullet:
    Image = None
    def __init__(self,x,y,power,angle,wind):
        self.x = x                      #초기위치
        self.y = y                      #초기위치
        self.moveX = 0                  #움직인위치
        self.moveY = 0                  #움직인위치
        self.speed = power
        self.angle = angle
        #self.v_x = power * cos(angle)   #x축속도
        #self.v_y = power * cos(angle)   #y축속도
        self.wind = wind
        self.time = 0.1                 #시간
        if Bullet.Image == None:
            Bullet.Image = load_image('image//Bullet1.png')
        self.frame = 0
    def update(self):
        self.time += 0.1
        self.frame = (self.frame + 1) % 4
        self.moveX = self.x + (self.speed * sin(pi * self.angle / 180)) * self.time + 0.5 * (self.wind / 10.0) * self.time * self.time
        self.moveY = self.y + (self.speed * cos(pi * self.angle / 180)) * self.time + 0.5 * (-0.98) * self.time * self.time
    def draw(self):
        self.Image.clip_draw(self.frame * 12,0,12,12,self.moveX,self.moveY)
        
    def draw_bb(self):
        draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.left, self.bottom, self.right, self.top