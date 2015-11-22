from CSoldier import *
from CBlock import *
from CAnimation import *
from math import *

collision_sound = None
item_sound =None

def get_distance(p1,p2):
    width = p1.x - p2.x
    height = p1.y - p2.y
    distance = sqrt(width*width + height*height)
    return distance
def calculate_damage(damage,distance,explosice_range):
    return damage - damage * (distance / explosice_range)

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def collision_bullet_and_obj(bullet,block,green,gray,item,animation,dead):
    collision_obj = False
    #collision_bullet = False
    
    for i in bullet:
        for j in block:
            if collide(i,j):
                collision_obj = True
                break
        for k in green:
            if collide(i,k):
                collision_obj = True
                break
        for l in gray:
            if collide(i,l):
                collision_obj = True
                break
    if collision_obj == True:
        global collision_sound
        if collision_sound == None:
            collision_sound = load_wav('sound//sound_rocket_explosion_1.ogg')
            collision_sound.set_volume(128)
        collision_sound.play()
        for i in bullet:
            distance = 0
            for j in block:
                distance = get_distance(i,j)
                if distance < i.getrange():
                    j.set_strength(calculate_damage(i.damage,distance,i.explosice_range))
                    #if j.get_strength() <= 0:
                    #    block.remove(j)
            for k in green:
                distance = get_distance(i,k)
                if distance < i.getrange():
                    k.set_hp(calculate_damage(i.damage,distance,i.explosice_range))
                    #if k.get_hp() <= 0:
                    #    green.remove(k)
            for l in gray:
                distance = get_distance(i,l)
                if distance < i.getrange():
                    l.set_hp(calculate_damage(i.damage,distance,i.explosice_range))
                    #if l.get_hp() <= 0:
                    #    gray.remove(l)
            for m in item:
                distance = get_distance(i,m)
                if distance < i.getrange():
                    m.set_hp(calculate_damage(i.damage,distance,i.explosice_range))
            animation.append(Explosion(i.x,i.y));
            bullet.remove(i)   
        return True
    for j in block:
        if j.get_strength() <= 0:
            block.remove(j)
    for k in green:
        if k.get_hp() <= 0:
            dead.play()
            green.remove(k)
            animation.append(Dead_Green(k.x,k.y));
    for l in gray:
        if l.get_hp() <= 0:
            dead.play()
            gray.remove(l)
            animation.append(Dead_Gray(l.x,l.y));
    for m in item:
        if m.get_hp() <= 0:
            item.remove(m)
    return False

def collision_soldier_and_item(soldier,item):
    global item_sound
    if item_sound == None:
        item_sound = load_wav('sound//item.wav')
        item_sound.set_volume(64)
    type = 0
    for i in item:
        if collide(soldier,i):
            item_sound.play()
            #print(i.type)
            type = i.type
            item.remove(i)
    return type

    

def collision_item_and_block(item,block):
    if collide(item,block):
       item.y = block.top + 10
       item.fall = False
       item.falltime = 0
    else:
        item.fall = True

def collision_soldier_and_block(soldier,block):
    if collide(soldier,block):
        if(soldier.right > block.left) and (soldier.left < block.right):
            if(soldier.bottom < block.top-0.1) and (soldier.bottom > block.top - 22):
                soldier.y = block.top + 30
                if soldier.jump:
                    soldier.state = SoldierState.Move
                    soldier.STATE = SoldierHandle.MOVE
                fall = False
                soldier.jump = False
                soldier.falltime = 0
            if(soldier.top > block.bottom) and (soldier.top < block.bottom + 22):
                if soldier.jump:
                    soldier.state = SoldierState.Move
                    soldier.STATE = SoldierHandle.MOVE
                soldier.jump = False


        if (soldier.y < block.top) and (soldier.y > block.bottom):
            if(soldier.right > block.left) and (soldier.right < block.left + 22):
                soldier.x = block.left - 10
            if(soldier.left < block.right) and (soldier.left > block.right - 22):
                soldier.x = block.right + 10