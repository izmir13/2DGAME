from pico2d import *
import game_framework
import game_state

class Menu:
    image_playgame = None
    image_howtoplay = None
    image_quit = None
    def __init__(self):
        if Menu.image_playgame == None:
            Menu.image_playgame = load_image('image//playgame.png')
        if Menu.image_howtoplay == None:
            Menu.image_howtoplay = load_image('image//howtoplay.png')
        if Menu.image_quit == None:
            Menu.image_quit = load_image('image//quit.png')
        self.image_x = 600
        self.image_play_y = 284
        self.image_htp_y = 242
        self.image_quit_y = 200
        self.select_menu = [1,0,0]
        self.menucount = 0
    def update(self):
        self.select_menu = [0,0,0]
        if (self.menucount == 0):
            self.select_menu[0] = 1
        if (self.menucount == 1):
            self.select_menu[1] = 1
        if (self.menucount == 2):
            self.select_menu[2] = 1

    def draw(self):
        self.image_playgame.clip_draw(245* self.select_menu[0],0,245,42, self.image_x,self.image_play_y,300,50);
        self.image_howtoplay.clip_draw(245* self.select_menu[1],0,245,42,self.image_x,self.image_htp_y,300,50);
        self.image_quit.clip_draw(245* self.select_menu[2],0,245,42,self.image_x,self.image_quit_y,300,50);

    def event(self,event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            self.menucount = (self.menucount + 1) % 3
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            self.menucount = (self.menucount - 1) % 3
        if((self.menucount == 0) and ((event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN))):
            game_framework.change_state(game_state)
        if((self.menucount == 1) and ((event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN))):
            game_framework.change_state(game_state)
        if((self.menucount == 2) and ((event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN))):
            game_framework.quit()