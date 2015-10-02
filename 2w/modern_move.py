from pico2d import *

def handle_events():
    global running
    global move_Right           #오른쪽으로 가는중
    global move_Left            #왼쪽으로 가는중
    global character_draw       #오른쪽?왼쪽?
    global character_state      #캐릭터 상태
    global state_frame          #상태에 따른 이미지 수
    global character_aim        #조준
    global frame

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:     #키를 눌렸을떄
            if event.key == SDLK_RIGHT:
                character_state = 240       #움직임
                state_frame = 6
                move_Right = True
                character_draw = True
                character_aim = False
            elif event.key == SDLK_LEFT:
                character_state = 240       #움직임
                state_frame = 6
                move_Left = True
                character_draw = False
                character_aim = False
            elif event.key == SDLK_SPACE:
                character_state = 160       #점프
                state_frame = 5
                character_aim = False
            elif event.key == SDLK_UP:      #조준
                character_state = 80
                state_frame = 8
                #character_aim = True
        elif event.type == SDL_KEYUP:       #키를 떘을때
            frame = 0
            if event.key == SDLK_RIGHT:
                character_state = 320       #대기상태
                state_frame = 5
                move_Right = False
            elif event.key == SDLK_LEFT:
                character_state = 320       #대기상태
                state_frame = 5
                move_Left = False
            elif event.key == SDLK_ESCAPE:
                running = False

def draw_character():
    if character_draw == True:
        character_R.clip_draw(frame * 60, character_state, 60, 80, character_x, 90)
    if character_draw == False:
        character_L.clip_draw(frame * 60, character_state, 60, 80, character_x, 90)

def move_character():
    global character_x
    if move_Right == True:
        character_x += 5
    if move_Left == True:
        character_x -= 5

def frame_character():
    global frame
    if character_aim == False:
        frame = (frame + 1) % state_frame
    elif character_aim == True:
        frame = (frame) % state_frame

open_canvas()
grass = load_image('grass.png')
character_L = load_image('ModernArmy_L.png')
character_R = load_image('ModernArmy_R.png')

running = True
move_Right = False
move_Left = False
character_draw = True
character_aim = False
character_state = 320   #idle_state
state_frame = 5         #idle_state
character_x = 50
frame = 0
while (running):
    clear_canvas()
    grass.draw(400, 30)
    draw_character()
    update_canvas()
    frame_character()

    delay(0.20)
    handle_events()
    move_character()

close_canvas()

