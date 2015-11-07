from pico2d import *

class CUI:
    power_bar_image = None
    power_gage_image = None
    #hp_bar_image = None
    #hp_gage_image = None
    def __init__(self):
        if CUI.power_bar_image == None:
            CUI.power_bar_image = load_image('image//power_bar.png')
        if CUI.power_gage_image == None:
            CUI.power_gage_image = load_image('image//power_gage1.png')
        #if CUI.hp_bar_image == None:
        #    CUI.hp_bar_image = load_image('image//hp_bar.png')
        #if CUI.hp_gage_image == None:
        #    CUI.hp_gage_image = load_image('image//hp_gage.png')

    def draw(self,power):
        self.power_bar_image.draw(600,50)
        self.power_gage_image.clip_draw(0,0,power,20,600,50)