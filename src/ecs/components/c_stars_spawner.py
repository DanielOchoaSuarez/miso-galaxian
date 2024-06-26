import pygame
import random


class CStarsSpawner:
    def __init__(self, screen_rect: pygame.Rect, starfield_cfg: dict) -> None:
        self.num_starts: int = starfield_cfg['number_of_stars']
        self.start_data: list = []
        self.screen_width: int = screen_rect.width
        self.screen_height: int = screen_rect.height
        for _ in range(0, self.num_starts):
            self.start_data.append(
                StarData(self.screen_width, self.screen_height, starfield_cfg))


class StarData:
    def __init__(self, screen_width: int, screen_height, cfg: dict) -> None:
        self.spawned: bool = False
        self.spawn_counter: int = 0
        self.blink_counter: float = 0.0
        self.spawn_at: int = random.randint(0, 15)
        self.entity_id: int = 0
        x_pos = StarData.get_random_pos(screen_width)
        y_pos = StarData.get_random_pos(screen_height)
        x_vel, y_vel = StarData.get_random_vel(
            cfg['vertical_speed']['min'], cfg['vertical_speed']['max'])
        r, g, b = StarData.get_random_col(cfg['star_colors'])
        w = StarData.get_random_size()
        self.pos: pygame.Vector2 = pygame.Vector2(x_pos, y_pos)
        self.vel: pygame.Vector2 = pygame.Vector2(x_vel, y_vel)
        self.col: pygame.color = pygame.Color(r, g, b)
        self.size: pygame.Vector2 = pygame.Vector2(w, w)
        self.blink: float = StarData.get_random_blink(
            cfg['blink_rate']['min'], cfg['blink_rate']['max'])

    @staticmethod
    def get_random_pos(screen_pos) -> int:
        x_pos = random.randint(5, screen_pos - 5)
        return x_pos

    @staticmethod
    def get_random_vel(min, max) -> int:
        y_vel = random.randint(min, max)
        x_vel = 0
        return x_vel, y_vel

    @staticmethod
    def get_random_blink(min, max) -> int:
        return random.uniform(min, max)

    @staticmethod
    def get_random_col(cfg: dict) -> int:
        choise = random.randint(0, len(cfg)-1)
        color = cfg[choise]
        return color['r'], color['g'], color['b']

    @staticmethod
    def get_random_size() -> int:
        return random.randint(1, 1)
