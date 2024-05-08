

import pygame
from src.create.background_creator import create_stars_spawner
from src.create.prefab_creator_interface import create_logo_title
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.systems.s_logo_title import system_logo_title
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_stars_spawner import system_stars_spawner
from src.engine.cfg_loader import interface_cfg
from src.engine.scenes.scene import Scene


class MenuScene(Scene):

    def do_create(self):
        self.interface_cfg = interface_cfg()

        create_stars_spawner(self.ecs_world, self.screen_rect)
        create_logo_title(self.ecs_world, self.interface_cfg['logo_title'])

        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action,
                                     CInputCommand("START_GAME", pygame.K_z))

    def do_update(self, delta_time: float):
        system_stars_spawner(self.ecs_world, delta_time,
                             self.screen_rect.height)
        system_movement(self.ecs_world, delta_time)
        system_logo_title(self.ecs_world)

    def do_action(self, action: CInputCommand):
        if action.name == "START_GAME":
            print('Cambio de escena a LEVEL_01')
            # self.switch_scene("LEVEL_01")
