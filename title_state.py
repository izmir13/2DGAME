import game_framework
import game_state
from pico2d import *
from CMenu import *

name = "TitleState"
image = None
squad_num = None
army = None
map = None
number_squad = None
number_map = None
select = 1
menu = None
menu_select = True
squad_select = False
map_select = False
map_num = None

title_bgm = None
move_bgm = None

def enter():
    global squad_num
    squad_num = 3
    global map_num
    map_num = 1
    global image
    image = load_image('image//MS_Title.png')
    global menu
    menu = Menu()
    global army
    army = Rest_Army(400,300)
    global map
    map = Map(800,300)
    global number_squad
    number_squad = Number(400,250)
    global number_map
    number_map = Number(800,250)
    global title_bgm
    title_bgm = load_music('sound//Unity.mp3')
    title_bgm.set_volume(64)
    title_bgm.repeat_play()
    global move_bgm
    move_bgm = load_wav('sound//move.wav')
    move_bgm.set_volume(24)

    #print(title_bgm,'\t',move_bgm)
    #print(title_bgm.get_volume(),'\t',move_bgm.get_volume())

def exit():
    game_state.squad_num = squad_num
    game_state.map_num = map_num
    global image
    del(image)
    global menu
    del(menu)
    global army
    del(army)
    global map
    del(map)
    global number_squad
    del(number_squad)
    global number_map
    del(number_map)
    #title_bgm.stop()
    global title_bgm
    del(title_bgm)
    global move_bgm
    del(move_bgm)

def handle_events(frame_time):
    global select
    global menu_select
    global squad_select
    global map_select
    global squad_num
    global map_num
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        if event.type == SDL_KEYDOWN:
            move_bgm.play()
        if event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            select = (select -1) % 3
            menu_select = False
        if event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            select = (select +1) % 3
            menu_select = False

        if select == 0:
            map_select = False
            squad_select = True
            if event.type == SDL_KEYDOWN and event.key == SDLK_UP:
                squad_num = (squad_num +1)
            if event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
                squad_num = (squad_num -1)
            if squad_num < 1:
                squad_num = 9
            if squad_num > 9:
                squad_num = 1

        if select == 2:
            squad_select = False
            map_select = True
            if event.type == SDL_KEYDOWN and event.key == SDLK_UP:
                map_num = map_num +1
            if event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
                map_num = map_num -1
            if map_num < 1:
                map_num = 3
            if map_num > 3:
                map_num = 1

        if select == 1:
            menu.event(event)
            menu_select = True
            squad_select = False
            map_select = False


def draw(frame_time):
    clear_canvas()
    image.draw(600,300)
    army.draw()
    map.draw()
    number_squad.draw()
    number_map.draw()
    menu.draw()
    update_canvas()

def update(frame_time):
    global menu_select
    global squad_select
    global map_select
    menu.update(menu_select)
    army.update(frame_time)
    number_squad.update(squad_select,squad_num)
    number_map.update(map_select,map_num)

def pause():
    pass

def resume():
    pass