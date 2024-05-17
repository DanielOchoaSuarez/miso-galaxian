import pygame
from enum import Enum


class CEnemyState():
    def __init__(self, pos: pygame.Vector2, vel: pygame.Vector2, chase: pygame.Vector2, score: int, chasing_score: int) -> None:
        self.state = EnemyState.IDLE
        self.army_pos = pos
        self.army_vel = vel
        self.vel_chase = chase
        self.score = score
        self.chasing_score = chasing_score
        self.allow_shoot_time = 1.5
        self.allow_shoot_time_counter = 0
        self.sound_played = False


class EnemyState(Enum):
    IDLE = 0
    MOVE = 1
    CHASING = 2
    LANDING = 3
