import game_framework
import title_state
from pico2d import *

name = "EndState"
image = None
winner = None
player_image = None
exit_image = None
retry_image = None
select = 1
end_bgm = None
move_bgm = None
def enter():
    global image
    global player_image
    global exit_image
    global retry_image
    image = load_image('image//ending_background.png')
    player_image = load_image('image//playernum.png')
    exit_image = load_image('image//ExitButton.png')
    retry_image = load_image('image//RetryButton.png')
    global end_bgm
    global move_bgm
    end_bgm = load_music('sound//end.ogg')
    move_bgm = load_wav('sound//move.wav')
    end_bgm.set_volume(64)
    move_bgm.set_volume(12)
    end_bgm.play()
    print(end_bgm.get_volume())

def exit():
    global image
    del(image)
    global player_image
    del(player_image)
    global exit_image
    del(exit_image)
    global retry_image
    del(retry_image)
    end_bgm.stop()

def handle_events(frame_time):
    global select
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        if event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            select = 1
            move_bgm.play()
        if event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            select = 0
            move_bgm.play()
        if select == 1 and event.type == SDL_KEYDOWN and event.key == SDLK_RETURN:
            game_framework.quit()
        if select == 0 and event.type == SDL_KEYDOWN and event.key == SDLK_RETURN:
            game_framework.push_state(title_state)

def draw(frame_time):
    global winner
    clear_canvas()
    image.draw(600,300)
    player_image.clip_draw(60*winner,0,60,60,620,337)
    exit_image.clip_draw(192*select,0,192,49,500,260)
    retry_image.clip_draw(192*((select+1)%2),0,192,49,700,260)
    update_canvas()

def update(frame_time):
    pass

def pause():
    pass

def resume():
    pass