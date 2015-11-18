from pico2d import *
import game_framework
import game_state

class Menu:
    image_playgame = None
    image_howtoplay = None
    image_quit = None
    image_htp = None
    htp_draw = False
    
    def __init__(self):
        if Menu.image_playgame == None:
            Menu.image_playgame = load_image('image//playgame.png')
        if Menu.image_howtoplay == None:
            Menu.image_howtoplay = load_image('image//howtoplay.png')
        if Menu.image_quit == None:
            Menu.image_quit = load_image('image//quit.png')
        if Menu.image_htp == None:
            Menu.image_htp = load_image('image//htp.png')
        
        self.image_x = 600
        self.image_play_y = 300
        self.image_htp_y = 240
        self.image_quit_y = 180
        self.select_menu = [1,0,0]
        self.menucount = 0
    def update(self,select):
        self.select_menu = [0,0,0]
        if select == True:
            if (self.menucount == 0):
                self.select_menu[0] = 1
            if (self.menucount == 1):
                self.select_menu[1] = 1
            if (self.menucount == 2):
                self.select_menu[2] = 1
        else:
            self.select_menu[0] = 0
            self.select_menu[1] = 0
            self.select_menu[2] = 0

    def draw(self):
        self.image_playgame.clip_draw(490* self.select_menu[0],0,490,84, self.image_x,self.image_play_y);
        self.image_howtoplay.clip_draw(490* self.select_menu[1],0,490,84,self.image_x,self.image_htp_y);
        #self.image_howtoplay.clip_draw(1020* self.select_menu[1],0,1020,175,self.image_x,self.image_htp_y);
        self.image_quit.clip_draw(490* self.select_menu[2],0,490,84,self.image_x,self.image_quit_y);
        if Menu.htp_draw:
            self.image_htp.draw(600,300)

    def event(self,event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            self.menucount = (self.menucount + 1) % 3
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            self.menucount = (self.menucount - 1) % 3
        if((self.menucount == 0) and ((event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN))):
            game_framework.change_state(game_state)
        if((self.menucount == 1) and ((event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN))):
            if Menu.htp_draw == False:
                Menu.htp_draw = True
            elif Menu.htp_draw == True:
                Menu.htp_draw = False
        if((self.menucount == 2) and ((event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN))):
            game_framework.quit()


class Rest_Army:
    TIME_PER_ACTION = 2.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 4
    Image = None
    def __init__(self,x,y):
        if Rest_Army.Image == None:
            Rest_Army.Image = load_image('image//soldier.png')
        self.x = x
        self.y = y
        self.total_frames = 0
        self.frame = 0

    def update(self,frame_time):
        self.total_frames += Rest_Army.FRAMES_PER_ACTION * Rest_Army.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 4

    def draw(self):
        self.Image.clip_draw(self.frame * 45,0,45,35,self.x,self.y,90,70)


class Map:
    Image = None
    def __init__(self,x,y):
        if Map.Image == None:
            Map.Image = load_image('image//map.png')

        self.x = x
        self.y = y
        self.frame = 0

    def draw(self):
        self.Image.draw(self.x,self.y)


class Number:
    Image_white = None
    Image_black = None
    def __init__(self,x,y):
        if Number.Image_white == None:
            Number.Image_white = load_image('image//number.png')
        if Number.Image_black == None:
            Number.Image_black = load_image('image//number_black.png')
        self.x = x
        self.y = y
        self.frame = 0
        self.select = False

    def update(self,select,number):
        self.frame = number % 10
        self.select = select

    def draw(self):
        if self.select == False:
            self.Image_white.clip_draw(self.frame * 33,0,33,33,self.x,self.y)
        if self.select == True:
            self.Image_black.clip_draw(self.frame * 33,0,33,33,self.x,self.y)