from pico2d import *

class CUI:
    power_bar_image = None
    power_gage_image = None
    flag = None
    play = None
    yellowlpanel = None
    bluelpanel = None
    ingame_time = None
    vs_image = None
    vs_hp_image = None
    hp1_image = None
    hp2_image = None
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
        if CUI.yellowlpanel == None:
            CUI.yellowlpanel = load_image('image//yellowlPanel.png')
        if CUI.bluelpanel == None:
            CUI.bluelpanel = load_image('image//bluePanel.png')
        if CUI.ingame_time == None:
            CUI.ingame_time = load_image('image//imgamenumber.png')
        if CUI.vs_image == None:
            CUI.vs_image = load_image('image//vs_image.png')
        if CUI.vs_hp_image == None:
            CUI.vs_hp_image = load_image('image//vs_hp.png')
        if CUI.hp1_image == None:
            CUI.hp1_image = load_image('image//hp3.png')
        if CUI.hp2_image == None:
            CUI.hp2_image = load_image('image//hp4.png')
        self.time10 = 0
        self.time01 = 0
        self.hp_green_persent = 0
        self.hp_gray_persent = 0

    def update(self,frame_time,wind,play_time,total_hp_green,total_hp_gray,squad_num):
        self.total_frames += CUI.FRAMES_PER_ACTION * CUI.ACTION_PER_TIME * frame_time
        self.flag_frame = int(self.total_frames) % 4
        self.play_frame = int(self.total_frames) % 16
        if wind > 0 :
            self.wind_right = 1
        else:
            self.wind_right = 0
        print(total_hp_green,'\t',total_hp_gray)
        #print(play_time)
        if play_time <= 15 and total_hp_green > 0 and total_hp_gray > 0:
            self.time01 = (15 - play_time) % 10
            self.time10 = int((15 - play_time) / 10)
        #print(play_time,'\t',self.time01,'\t',self.time10)
        self.hp_green_persent = total_hp_green / (squad_num * 49) * 100
        self.hp_gray_persent = total_hp_gray / (squad_num * 49) * 100

    def draw(self,power,frame_time,play_x,play_y):
        self.power_bar_image.draw(600,50)
        self.yellowlpanel.draw(1150,50)
        self.vs_image.draw(600,550)

        self.hp1_image.clip_draw_to_origin(0,0,int(self.hp_green_persent*4.5),50,125,525)
        self.hp2_image.clip_draw_to_origin(0,0,int(self.hp_gray_persent*4.5),50,625,525)
        self.vs_hp_image.draw(350,550)
        self.vs_hp_image.draw(850,550)
        
        self.bluelpanel.draw(50,50)
        self.power_gage_image.clip_draw(0,0,power*2,20,600,50)
        self.flag.clip_draw(self.flag_frame * 64,self.wind_right * 64,64,64,50,45)
        self.play.clip_draw(self.play_frame * 28,0,28,17,play_x,play_y)
        if self.time10 != 0:
            self.ingame_time.clip_draw((9 - self.time01) * 56,0,56,90,1161,50)
            self.ingame_time.clip_draw((9 - self.time10) * 56,0,56,90,1109,50)
        else:
            self.ingame_time.clip_draw((9 - self.time01) * 56,0,56,90,1150,50)