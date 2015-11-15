import game_framework
import game_state
from pico2d import *

from CMenu import *

name = "TitleState"
image = None

def enter():
    global image
    image = load_image('image//MS_Title.png')
    global menu
    menu = Menu()

def exit():
    global image
    del(image)
    global menu
    del(menu)


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            menu.event(event)


def draw(frame_time):
    clear_canvas()
    image.draw(600,300)
    menu.draw()
    update_canvas()

def update(frame_time):
    menu.update()

def pause():
    pass

def resume():
    pass