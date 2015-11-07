class SoldierState:
    Idle = 320
    Move = 240
    Jump = 160
    Aim = 80
    Shoot = 0

class SoldierFrame:
    Idle = 5
    Move = 6
    Jump = 5
    Aim = 8
    Shoot = 8

class SoldierTeam:
    Green = 0
    Gray = 1

class Direction:
    Left = 0
    Right = 1

class SoldierHandle:
    MOVE = 0
    AIM = 1
    IDLE = 2