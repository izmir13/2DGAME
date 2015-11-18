from pico2d import *
from math import *
from myenum import *
import random
from CBullet import *

class Soldier:
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    greenteam_right_image = None
    greenteam_left_image = None
    grayteam_right_image = None
    grayteam_left_image = None
    hp_image = None
    aim_image = None 
    SOLDIER_MOVE = SoldierHandle.MOVE
    SOLDIER_AIM = SoldierHandle.AIM
    SOLDIER_IDLE = SoldierHandle.IDLE
    def __init__(self,team,pos):
        self.pos = random.randint(0,len(pos)-1)
        #print(self.pos)
        self.x = pos[self.pos].x#random.randint(10,2400)
        self.y = pos[self.pos].y#random.randint(100,1120)
        #self.x = random.randint(10,2400)
        #self.y = random.randint(100,1120)
        if team == SoldierTeam.Green:                                          # teamGreen
            if Soldier.greenteam_right_image == None:
                Soldier.greenteam_right_image = load_image('image//ModernArmy_R_1.png')
            if Soldier.greenteam_left_image == None:
                Soldier.greenteam_left_image = load_image('image//ModernArmy_L_1.png')
        if team == SoldierTeam.Gray:                                          # teamGray
            if Soldier.grayteam_right_image == None:
                Soldier.grayteam_right_image = load_image('image//ModernArmy_R_2.png')
            if Soldier.grayteam_left_image == None:
                Soldier.grayteam_left_image = load_image('image//ModernArmy_L_2.png')
        if Soldier.aim_image == None:
            Soldier.aim_image = load_image('image//aim.png')
        if Soldier.hp_image == None:
            Soldier.hp_image = load_image('image//hpbar1.png')
        self.dir = random.randint(Direction.Left,Direction.Right)
        self.state = SoldierState.Idle
        self.STATE = self.SOLDIER_IDLE
        self.moveRight = False
        self.moveLeft = False
        self.characterframe = SoldierFrame.Idle
        self.total_frames = 0
        self.frame = random.randint(0,SoldierState.Idle)#320
        self.angle = -90
        self.increAngel = False
        self.decreAngel = False
        self.power = 0.0
        self.charge = False
        self.team = team

        self.jump = False

        self.fall = True
        self.falltime = 0

        self.left = self.x-15
        self.right = self.x+15
        self.bottom = self.y-30
        self.top = self.y+10

        self.hp = 49
        self.shot = Shot.Normal

    def get_power(self):
        return self.power
    def set_hp(self,damage):
        self.hp -= damage
    def get_hp(self):
        return self.hp
   
    def handle_soldier_idle(self,frame_time):      #가만히 있을때
        self.total_frames += self.characterframe * Soldier.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % self.characterframe

    def handle_soldier_move(self,frame_time):      #움직일때
        self.fall = True
        self.total_frames += self.characterframe * Soldier.ACTION_PER_TIME * frame_time
        if self.jump:
            self.frame = int(self.total_frames) % self.characterframe
            self.y += 300 * frame_time
        else:
            self.frame = int(self.total_frames) % self.characterframe
        if self.moveRight:
            self.x += 100 * frame_time
        if self.moveLeft:
            self.x -= 100 * frame_time

    def handle_soldier_aim(self,frame_time):       #조준일때
        temp = 0        
        if self.angle <= 0:     #각도를 양수로 초기화.
            temp = -self.angle
        else:
            temp = self.angle
        if temp <= 22.5:
            self.frame = 7
        elif temp > 22.5 and temp <= 45:
            self.frame = 6
        elif temp > 45 and temp <= 67.5:
            self.frame = 5
        elif temp > 67.5 and temp <= 90:
            self.frame = 4
        elif temp > 90 and temp <= 112.5:
            self.frame = 3
        elif temp > 112.5 and temp <= 135:
            self.frame = 2
        elif temp > 135 and temp <= 157.5:
            self.frame = 1
        elif temp > 157.5:
                self.frame = 0
        
        if self.angle <= -180:
            self.angle = -180
        if self.angle >= 180:
            self.angle = 180
        if self.dir == Direction.Left:     # -180 ~ 0 일때 (왼쪽)
            if self.angle >= 0:
                self.angle *= -1
        if self.dir == Direction.Right:
            if self.angle <= 0:
                self.angle *= -1

        if self.increAngel:
            self.angle += 100 * frame_time
        if self.decreAngel:
            self.angle -= 100 * frame_time
        if self.charge:
            self.power += 50 * frame_time
            if self.power >= 125:
                self.power = 125
    handle_state = {
                SOLDIER_MOVE: handle_soldier_move,
                SOLDIER_AIM: handle_soldier_aim,
                SOLDIER_IDLE: handle_soldier_idle
    }

    def update(self,frame_time,item_type):
        if item_type != 0:
            if item_type == ItemType.Potion:
                self.hp += 10
                if self.hp >= 49:
                    self.hp = 49
            if item_type == ItemType.double_shot:
                self.shot = Shot.double
            if item_type == ItemType.triple_shot:
                self.shot = Shot.triple


        if self.fall:
            self.falltime += 5 * frame_time
            self.y = self.y + ((-0.98) * self.falltime * self.falltime)

        self.left = self.x-10
        self.right = self.x+10
        self.bottom = self.y-30
        self.top = self.y+10
        self.handle_state[self.STATE](self,frame_time)

    def draw(self,scroll_x,scroll_y):
        if self.x + scroll_x > -50 and self.x + scroll_x < 1250 and self.y + scroll_y > -50 and self.y + scroll_y < 650:
            if self.team == SoldierTeam.Green:
                if self.dir:
                    self.greenteam_right_image.clip_draw(self.frame * 60, self.state, 60, 80, self.x + scroll_x, self.y + scroll_y)
                else:
                    self.greenteam_left_image.clip_draw(self.frame * 60, self.state, 60, 80, self.x + scroll_x, self.y + scroll_y)
            elif self.team == SoldierTeam.Gray:
                if self.dir:
                    self.grayteam_right_image.clip_draw(self.frame * 60, self.state, 60, 80, self.x + scroll_x, self.y + scroll_y)
                else:
                    self.grayteam_left_image.clip_draw(self.frame * 60, self.state, 60, 80, self.x + scroll_x, self.y + scroll_y)

            if self.STATE == self.SOLDIER_AIM:
                self.aim_image.draw(self.x + scroll_x + 50 * sin(pi * self.angle / 180),self.y + scroll_y + 50 * cos(pi * self.angle / 180))
                #self.aim_image.clip_draw(36,0,12,12,self.x + scroll_x + 50 * sin(pi * self.angle / 180),self.y + scroll_y + 50 * cos(pi * self.angle / 180))

            self.hp_image.clip_draw(0,(int(self.hp/10))*7,50,7,self.x + scroll_x,self.y-50 + scroll_y)

    def event(self,event,bullet,wind):
        if event.type == SDL_KEYDOWN:   #키가 눌렸을때
            if event.key == SDLK_RIGHT:                             #   →
                self.dir = Direction.Right
                self.moveRight = True
                self.characterframe = SoldierFrame.Move
                self.state = SoldierState.Move
                self.STATE = self.SOLDIER_MOVE
            if event.key == SDLK_LEFT:                              #   ←
                self.dir = Direction.Left
                self.moveLeft = True
                self.characterframe = SoldierFrame.Move
                self.state = SoldierState.Move
                self.STATE = self.SOLDIER_MOVE
            if event.key == SDLK_UP:                                #   ↑
                self.characterframe = SoldierFrame.Aim
                self.state = SoldierState.Aim
                self.STATE = self.SOLDIER_AIM
                if self.dir == Direction.Right:
                    self.decreAngel = True
                if self.dir == Direction.Left:
                    self.increAngel = True
            if event.key == SDLK_DOWN:                              #   ↓
                self.characterframe = SoldierFrame.Aim
                self.state = SoldierState.Aim
                self.STATE = self.SOLDIER_AIM
                if self.dir == Direction.Right:
                    self.increAngel = True
                if self.dir == Direction.Left:
                    self.decreAngel = True
            if (event.key == SDLK_LCTRL):       
                self.jump = True                      
                self.frame = 0
                self.characterframe = SoldierFrame.Jump
                self.state = SoldierState.Jump
                self.STATE = self.SOLDIER_MOVE
            if event.key == SDLK_SPACE and self.state == SoldierState.Aim:
                self.charge = True

        if event.type == SDL_KEYUP:     #키를 땠을때
            if event.key == SDLK_RIGHT:                             #   →
                self.dir = Direction.Right
                self.moveRight = False
                self.characterframe = SoldierFrame.Idle
                self.state = SoldierState.Idle
                self.STATE = self.SOLDIER_IDLE
                self.frame = 0                                               
            if event.key == SDLK_LEFT:                              #   ←
                self.dir = Direction.Left
                self.moveLeft = False
                self.characterframe = SoldierFrame.Idle
                self.state = SoldierState.Idle
                self.STATE = self.SOLDIER_IDLE                                      
                self.frame = 0
            if (event.key == SDLK_UP) or (event.key == SDLK_DOWN):  #   ↑  ↓
                self.frame = 0#?
                self.increAngel = False
                self.decreAngel = False
            if event.key == SDLK_SPACE and self.state == SoldierState.Aim:
                self.charge = False
                
                if self.shot == Shot.Normal:
                    bullet.append(Bullet(self.x + sin(pi * self.angle / 180)*30 ,self.y + cos(pi * self.angle / 180)*30, self.power,self.angle,wind))                                        
                elif self.shot == Shot.double:
                    bullet.append(Bullet(self.x + sin(pi * self.angle / 180)*30 ,self.y + cos(pi * self.angle / 180)*30, self.power-3,self.angle,wind))
                    bullet.append(Bullet(self.x + sin(pi * self.angle / 180)*30 ,self.y + cos(pi * self.angle / 180)*30, self.power+3,self.angle,wind))
                elif self.shot == Shot.triple:
                    bullet.append(Bullet(self.x + sin(pi * self.angle / 180)*30 ,self.y + cos(pi * self.angle / 180)*30, self.power,self.angle-5,wind))
                    bullet.append(Bullet(self.x + sin(pi * self.angle / 180)*30 ,self.y + cos(pi * self.angle / 180)*30, self.power,self.angle,wind))
                    bullet.append(Bullet(self.x + sin(pi * self.angle / 180)*30 ,self.y + cos(pi * self.angle / 180)*30, self.power,self.angle+5,wind))
                self.power = 0
                self.characterframe = SoldierFrame.Idle
                self.state = SoldierState.Idle
                self.STATE = self.SOLDIER_IDLE
                self.moveRight = False
                self.moveLeft = False
                self.shot = Shot.Normal
                #if self.team == SoldierTeam.Green:
                #    Soldier.team1_turn = (Soldier.team1_turn + 1) % 3
                #    Soldier.GAME_TURN = 2
                #elif self.team == SoldierTeam.Gray:
                #    Soldier.team2_turn = (Soldier.team2_turn + 1) % 3
                #    Soldier.GAME_TURN = 1
    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.left, self.bottom, self.right, self.top