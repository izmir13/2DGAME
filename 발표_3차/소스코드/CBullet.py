from pico2d import *
from math import *

class Bullet:
    Image = None
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 4
    def __init__(self,x,y,power,angle,wind):
        self.first_x = x                      #초기위치
        self.first_y = y                      #초기위치
        self.x = self.first_x                  #움직인좌표
        self.y = self.first_y                  #움직인좌표
        self.speed = power
        self.angle = angle
        #self.v_x = power * cos(angle)   #x축속도
        #self.v_y = power * cos(angle)   #y축속도
        self.wind = wind
        self.time = 0.1                 #시간
        if Bullet.Image == None:
            Bullet.Image = load_image('image//Bullet1.png')
        self.total_frames = 0
        self.frame = 0

        self.left = self.x-6
        self.right = self.x+6
        self.bottom = self.y-6
        self.top = self.y+6

        self.damage = 30
        self.explosice_range = 100
    
    def getdamage(self):
        return self.damage
    def getrange(self):
        return self.explosice_range

    def update(self,frame_time):
        self.left = self.x-6
        self.right = self.x+6
        self.bottom = self.y-6
        self.top = self.y+6

        self.time += 10 * frame_time
        self.total_frames += Bullet.FRAMES_PER_ACTION * Bullet.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 4
        self.x = self.first_x + ((self.speed * sin(pi * self.angle / 180)) * self.time + 0.5 * (self.wind / 10.0) * self.time * self.time)
        self.y = self.first_y + ((self.speed * cos(pi * self.angle / 180)) * self.time + 0.5 * (-4.9) * self.time * self.time)

    def draw(self,scroll_x,scroll_y):
        self.Image.clip_draw(self.frame * 12,0,12,12,self.x + scroll_x,self.y + scroll_y,15,15)
        #draw_rectangle(self.x - self.explosice_range/2,self.y - self.explosice_range/2, self.x + self.explosice_range/2,self.y + self.explosice_range/2)
    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.left, self.bottom, self.right, self.top