import pygame
import esper
from enum import Enum

from src.ecs.components.c_input_command import CInputCommand
from src.ecs.systems.s_input import system_input
from src.ecs.systems.s_rendering import system_rendering
import src.engine.game_engine


class MenuSceneState(Enum):
    LOADING = 1
    READY = 2


class Scene:
    def __init__(self, game_engine: 'src.engine.game_engine.GameEngine') -> None:
        self.ecs_world = esper.World()
        self._game_engine: src.engine.game_engine.GameEngine = game_engine
        self.screen_rect: pygame.Rect = self._game_engine.screen.get_rect()
        self.is_paused: bool = False
        self.menu_state = MenuSceneState.LOADING

    def do_process_events(self, event: pygame.event):
        system_input(self.ecs_world, event, self.do_action)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self.is_paused = not self.is_paused

    def simulate(self, delta_time):
        self.do_update(delta_time)
        self.ecs_world._clear_dead_entities()

    def clean(self):
        self.ecs_world.clear_database()
        self.do_clean()

    def switch_scene(self, new_scene_name: str):
        self._game_engine.switch_scene(new_scene_name)

    def do_create(self):
        pass

    def do_update(self, delta_time: float):
        pass

    def do_draw(self, screen):
        system_rendering(self.ecs_world, screen)

    def do_action(self, action: CInputCommand):
        pass

    def do_clean(self):
        pass