import game_framework
import title_state
from pico2d import *

name = "StartState"
image = None
logo_time = 0.0

def enter():
    global image
    open_canvas(1200,600)
    image = load_image('kpu_credit.png')

def exit():
    global image
    del(image)
    close_canvas()

def update():
    global logo_time

    if(logo_time > 0.1):
        logo_time = 0
        #game_framework.quit()
        game_framework.push_state(title_state)
    delay(0.01)
    logo_time += 0.01

def draw():
    global image
    clear_canvas()
    image.draw(600,300)
    update_canvas()

def handle_events():
    events = get_events()
    pass

def pause(): pass

def resume(): pass




