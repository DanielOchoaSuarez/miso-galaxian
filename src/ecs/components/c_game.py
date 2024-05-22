import pygame


class CGame:
    def __init__(self) -> None:
        self.life_respawn: int = 3
        self.time_to_respawn: int = 2
        self.respawn_counter: int = 0
        self.is_respawning: bool = False
        self.score: int = 0
        self.update_score: bool = False
