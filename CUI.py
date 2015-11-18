from pico2d import *

class CUI:
    power_bar_image = None
    power_gage_image = None
    flag = None
    play = None
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 4
    total_frames = 0
    flag_frame = 0
    play_frame = 0
    wind_right = 0
    #hp_bar_image = None
    #hp_gage_image = None
    def __init__(self):
        if CUI.power_bar_image == None:
            CUI.power_bar_image = load_image('image//power_bar.png')
        if CUI.power_gage_image == None:
            CUI.power_gage_image = load_image('image//power_gage1.png')
        if CUI.flag == None:
            CUI.flag = load_image('image//flag.png')
        if CUI.play == None:
            CUI.play = load_image('image//play.png')
        #if CUI.hp_bar_image == None:
        #    CUI.hp_bar_image = load_image('image//hp_bar.png')
        #if CUI.hp_gage_image == None:
        #    CUI.hp_gage_image = load_image('image//hp_gage.png')

    def update(self,frame_time,wind):
        self.total_frames += CUI.FRAMES_PER_ACTION * CUI.ACTION_PER_TIME * frame_time
        self.flag_frame = int(self.total_frames) % 4
        self.play_frame = int(self.total_frames) % 16
        if wind > 0 :
            self.wind_right = 1
        else:
            self.wind_right = 0

    def draw(self,power,frame_time,play_x,play_y):
        self.power_bar_image.draw(600,50)
        self.power_gage_image.clip_draw(0,0,power*2,20,600,50)
        self.flag.clip_draw(self.flag_frame * 64,self.wind_right * 64,64,64,100,500)
        self.play.clip_draw(self.play_frame * 28,0,28,17,play_x,play_y)