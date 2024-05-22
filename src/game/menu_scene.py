import pygame


from src.create.background_creator import create_stars_spawner
from src.create.prefab_creator_interface import TextAlignment, create_logo_title, create_menu_text
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_menu_object import CMenuObject
from src.ecs.systems.s_menu_object import system_menu_object
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_stars_spawner import system_stars_spawner
from src.engine.cfg_loader import interface_cfg, starfield_cfg, window_cfg
from src.engine.scenes.scene import MenuSceneState, Scene
from src.engine.service_locator import ServiceLocator


class MenuScene(Scene):

    def do_create(self):
        title, size, framerate, bg_color = window_cfg()
        self.starfield_cfg = starfield_cfg()
        self.interface_cfg = interface_cfg()

        create_stars_spawner(
            self.ecs_world, self.screen_rect, self.starfield_cfg)

        # Logo Title
        create_logo_title(self.ecs_world, size['h'], self.interface_cfg)

        # Press Start
        create_menu_text(
            self.ecs_world, size['h'], self.interface_cfg, 'press_start_text', TextAlignment.CENTER)

        # Player score
        create_menu_text(
            self.ecs_world, size['h'], self.interface_cfg, 'label_player_text', TextAlignment.CENTER)
        create_menu_text(
            self.ecs_world, size['h'], self.interface_cfg, 'player_score_text', TextAlignment.RIGHT)

        # High Score
        create_menu_text(
            self.ecs_world, size['h'], self.interface_cfg, 'label_high_score_text', TextAlignment.CENTER)
        create_menu_text(
            self.ecs_world, size['h'], self.interface_cfg, 'high_score_text', TextAlignment.RIGHT)

        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action,
                                     CInputCommand("START_GAME", pygame.K_z))

    def do_update(self, delta_time: float):
        system_stars_spawner(self.ecs_world, delta_time,
                             self.screen_rect.height)
        system_movement(self.ecs_world, delta_time, False)
        system_menu_object(self.ecs_world, delta_time, self.menu_state)

    def do_action(self, action: CInputCommand):

        menu_components = self.ecs_world.get_component(CMenuObject)
        all_scrolled = all(
            c_m.is_scrolled for _, c_m in menu_components)
        if all_scrolled:
            self.menu_state = MenuSceneState.READY

        if action.name == "START_GAME" and action.phase == CommandPhase.END:
            if self.menu_state == MenuSceneState.LOADING:
                self.menu_state = MenuSceneState.READY
            else:
                ServiceLocator.sounds_service.play(self.interface_cfg['game_start'])
                self.switch_scene("LEVEL_01")