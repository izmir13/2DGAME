from pico2d import *
from myenum import *
import random

class Weapon:
    Image = None
    TIME_PER_ACTION = 2.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 9
    def __init__(self,x,y):  
        self.x = x                      #초기위치
        self.y = y                      #초기위치
        if Weapon.Image == None:
            Weapon.Image = load_image('image//item.png')
        self.total_frames = 0
        self.frame = 0
        self.fall = True
        self.falltime = 0
        self.left = self.x-12
        self.right = self.x+10
        self.bottom = self.y-15
        self.top = self.y+10
        self.hp = 5
        self.type = random.randint(ItemType.double_shot,ItemType.triple_shot) 

    def update(self,frame_time):
        self.left = self.x-12
        self.right = self.x+10
        self.bottom = self.y-15
        self.top = self.y+10

        if self.fall:
            self.falltime += 5 * frame_time
            self.y = self.y + ((-0.98) * self.falltime * self.falltime)
        self.total_frames += Weapon.FRAMES_PER_ACTION * Weapon.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % self.FRAMES_PER_ACTION

    def draw(self):
        self.Image.clip_draw(self.frame * 31,0,31,30,self.x,self.y)

    def set_hp(self,damage):
        self.hp -= damage
    def get_hp(self):
        return self.hp

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.left, self.bottom, self.right, self.top



class Potion:
    Image = None
    TIME_PER_ACTION = 2.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 16
    def __init__(self,x,y):  
        self.x = x                      #초기위치
        self.y = y                      #초기위치
        if Potion.Image == None:
            Potion.Image = load_image('image//potion.png')
        self.total_frames = 0
        self.frame = 0
        self.fall = True
        self.falltime = 0
        self.left = self.x-6
        self.right = self.x+6
        self.bottom = self.y-8
        self.top = self.y+8
        self.hp = 5
        self.type = ItemType.Potion

    def update(self,frame_time):
        self.left = self.x-6
        self.right = self.x+6
        self.bottom = self.y-15
        self.top = self.y+8

        if self.fall:
            self.falltime += 5 * frame_time
            self.y = self.y + ((-0.98) * self.falltime * self.falltime)
        self.total_frames += Potion.FRAMES_PER_ACTION * Potion.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % self.FRAMES_PER_ACTION

    def set_hp(self,damage):
        self.hp -= damage
    def get_hp(self):
        return self.hp

    def draw(self):
        self.Image.clip_draw(self.frame * 15,0,15,24,self.x,self.y)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.left, self.bottom, self.right, self.top