import pygame
import random


class CStarsSpawner:
    def __init__(self, screen_rect: pygame.Rect) -> None:
        self.num_starts: int = 100
        self.max_vel: int = 80
        self.start_data: list = []
        self.screen_width: int = screen_rect.width
        for _ in range(0, self.num_starts):
            self.start_data.append(StarData(self.screen_width, self.max_vel))


class StarData:
    def __init__(self, screen_width: int, max_vel: int) -> None:
        self.spawned: bool = False
        self.spawn_counter: int = 0
        self.spawn_at: int = random.randint(0, 20)
        self.entity_id: int = 0
        x_pos, y_pos = StarData.get_random_pos(screen_width)
        x_vel, y_vel = StarData.get_random_vel(max_vel)
        r, g, b = StarData.get_random_col()
        w = StarData.get_random_size()
        self.pos: pygame.Vector2 = pygame.Vector2(x_pos, y_pos)
        self.vel: pygame.Vector2 = pygame.Vector2(x_vel, y_vel)
        self.col: pygame.color = pygame.Color(r, g, b)
        self.size: pygame.Vector2 = pygame.Vector2(w, w)

    @staticmethod
    def get_random_pos(screen_width) -> int:
        x_pos = random.randint(5, screen_width - 5)
        y_pos = 0
        return x_pos, y_pos

    @staticmethod
    def get_random_vel(max_vel) -> int:
        y_vel = random.randint(5, max_vel)
        x_vel = 0
        return x_vel, y_vel

    @staticmethod
    def get_random_col() -> int:
        r = random.randint(240, 255)
        g = random.randint(240, 255)
        b = random.randint(240, 255)
        return r, g, b

    @staticmethod
    def get_random_size() -> int:
        w = random.randint(1, 2)
        return w
