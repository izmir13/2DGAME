from pico2d import *
#from game_framework import *

class Block:
    Image = None
    def __init__(self, x, y, type):
        if Block.Image == None:
            Block.Image = load_image('image//Block.png')
        self.x = x
        self.y = y
        self.type = type
        self.strength = 3

        self.left = x-23
        self.right = x+21
        self.bottom = y-22
        self.top = y+22
    def draw(self):
        self.Image.clip_draw((self.strength - 3) * 45,self.type * 45,45,45,self.x,self.y)
        
    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.left, self.bottom, self.right, self.top