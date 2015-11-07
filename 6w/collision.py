from CSoldier import *
from CBlock import *

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def collision_soldier_and_block(soldier,block):
    if collide(soldier,block):
        if(soldier.right > block.left) and (soldier.left < block.right):
            if(soldier.bottom < block.top) and (soldier.bottom > block.top - 22):
                soldier.y = block.top + 31
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