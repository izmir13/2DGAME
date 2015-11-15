from pico2d import *

class Explosion:
    Image = None
    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 26
    def __init__(self,x,y):
        if Explosion.Image == None:
            Explosion.Image = load_image('image//Explosion.png')
        self.x = x
        self.y = y
        self.total_frames = 0
        self.frame = 0

    def update(self,frame_time):
        self.total_frames += Explosion.FRAMES_PER_ACTION * Explosion.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 26

    def draw(self,scroll_x,scroll_y):
        self.Image.clip_draw(self.frame * 58,0,58,64,self.x + scroll_x,self.y + scroll_y,100,100)


class Dead:
    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 12

class Dead_Green(Dead):
    Image = None
    def __init__(self,x,y):
        if Dead_Green.Image == None:
            Dead_Green.Image = load_image('image//army_dead_Green.png')
        self.x = x
        self.y = y
        self.total_frames = 0
        self.frame = 0

    def update(self,frame_time):
        self.total_frames += Dead.FRAMES_PER_ACTION * Dead.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 26

    def draw(self,scroll_x,scroll_y):
        self.Image.clip_draw(self.frame * 54,0,54,60,self.x + scroll_x,self.y + scroll_y)

class Dead_Gray(Dead):
    Image = None
    def __init__(self,x,y):
        if Dead_Gray.Image == None:
            Dead_Gray.Image = load_image('image//army_dead_Gray.png')
        self.x = x
        self.y = y
        self.total_frames = 0
        self.frame = 0

    def update(self,frame_time):
        self.total_frames += Dead.FRAMES_PER_ACTION * Dead.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 26

    def draw(self,scroll_x,scroll_y):
        self.Image.clip_draw(self.frame * 54,0,54,60,self.x + scroll_x,self.y + scroll_y)