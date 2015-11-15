from pico2d import *
import random
#from game_framework import *

class Block:
    Image = None
    def __init__(self, x, y, type):
        if Block.Image == None:
            Block.Image = load_image('image//Block1.png')
        self.x = x
        self.y = y
        self.type = type
        self.strength = random.randint(5,25)

        self.left = x-23
        self.right = x+21
        self.bottom = y-22
        self.top = y+22

    def set_strength(self,damage):
        self.strength -= damage
    def get_strength(self):
        return self.strength

    def draw(self,scroll_x,scroll_y):
        self.Image.clip_draw(int(self.strength/10) * 45,self.type * 45,45,45,self.x + scroll_x,self.y + scroll_y)
        
    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.left, self.bottom, self.right, self.top