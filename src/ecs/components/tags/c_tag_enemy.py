import pygame
from enum import Enum

class CTagEnemy():
    def __init__(self, pos:pygame.Vector2) -> None:
        self.state = EnemyState.MOVE
        self.init_pos = pos

class EnemyState(Enum):
    IDLE = 0
    MOVE = 1