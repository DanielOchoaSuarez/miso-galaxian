import pygame
import src

from src.create.background_creator import create_stars_spawner
from src.create.enemy_player_creator import create_enemy_spawner, create_game, create_input_player, create_player, create_player_bullet
from src.create.prefab_creator_interface import TextAlignment, TypeText, create_endgame_text, create_game_text, create_img_lives, create_level_text, create_lives
from src.ecs.components.c_endgame import CEndGameText
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_menu_object import CMenuObject
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.systems.s_animations import system_animation
from src.ecs.systems.s_bullet_limits import system_bullet_limits
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_collision_bullet_enemy_player import system_collision_bullet_enemy_player
from src.ecs.systems.s_collision_enemy_player import system_collision_enemy_player
from src.ecs.systems.s_enemy_chasing import system_enemy_chasing
from src.ecs.systems.s_enemy_idle_movement import system_enemy_idle_movement
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_enemy_state import system_enemy_state
from src.ecs.systems.s_explosion_state import system_explosion_state
from src.ecs.systems.s_lives import system_lives
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.system_game_interface import system_game_interface
from src.ecs.systems.s_player_limits import system_player_limits
from src.ecs.systems.s_respawn_player import system_respawn_player
from src.ecs.systems.s_stars_spawner import system_stars_spawner
from src.engine.cfg_loader import interface_cfg, level_cfg, player_cfg, starfield_cfg, enemy_cfg, explosion_cfg
from src.engine.scenes.scene import Scene
from src.engine.service_locator import ServiceLocator


class PlayScene(Scene):

    def __init__(self, level: str, engine: 'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)
        self.player = player_cfg()
        self.starfield_cfg = starfield_cfg()
        self.level_cfg = level_cfg(level)
        self.enemy_cfg = enemy_cfg()
        self.explosion_cfg = explosion_cfg()
        self.interface_cfg = interface_cfg()
        self.player_entity = None
        self._player_tag  = None
        self._c_game_entity  = None
        self._player_cv = None
        self.spawn_player_wait = 2
        self.spawn_counter = 0
        self._lives_entity = None
        self._leveltimecounter = 0

    def do_create(self):
        self._c_game_entity = create_game(self.ecs_world)
        self._lives_entity = create_lives(self.ecs_world)
        create_stars_spawner(self.ecs_world, self.screen_rect, self.starfield_cfg)
        self.spawn_player()
        create_input_player(self.ecs_world)
        create_enemy_spawner(self.ecs_world, self.screen_rect)

        # Paused text
        create_game_text(self.ecs_world, self.interface_cfg, 'paused_text', TextAlignment.CENTER, TypeText.NA, 0)

        # Player score
        create_game_text(
            self.ecs_world, self.interface_cfg, 'label_player_text', TextAlignment.CENTER, TypeText.NA)
        create_game_text(
            self.ecs_world, self.interface_cfg, 'player_score_text', TextAlignment.RIGHT, TypeText.SCORE)

        # High Score
        create_game_text(
            self.ecs_world, self.interface_cfg, 'label_high_score_text', TextAlignment.CENTER, TypeText.NA)
        create_game_text(
            self.ecs_world, self.interface_cfg, 'high_score_text', TextAlignment.RIGHT, TypeText.HIGH_SCORE)
        
        # Lives
        create_img_lives(self.ecs_world, self.interface_cfg, self._lives_entity)

    def do_update(self, delta_time: float):
        system_stars_spawner(self.ecs_world, delta_time,
                            self.screen_rect.height)
        system_movement(self.ecs_world, delta_time, self.is_paused)
        system_game_interface(self.ecs_world, self.interface_cfg, delta_time, self.is_paused, self._c_game_entity)
        system_lives(self.ecs_world, self.interface_cfg, self._lives_entity)

        if not self.is_paused:
            system_player_limits(self.ecs_world, self.screen_rect)
            system_bullet_limits(
                self.ecs_world, self.screen_rect)
            system_enemy_spawner(self.ecs_world, self.screen_rect, self.enemy_cfg)
            system_enemy_state(self.ecs_world, self.screen_rect, self.player_entity, delta_time, self.level_cfg)
            system_enemy_idle_movement(self.ecs_world, self.screen_rect, delta_time)
            system_enemy_chasing(self.ecs_world, delta_time, self.player_entity, self.screen_rect)
            system_collision_bullet_enemy(self.ecs_world, self.explosion_cfg['enemy'], self._c_game_entity)
            system_collision_bullet_enemy_player(self.ecs_world, self.explosion_cfg['player'], self._lives_entity)
            system_collision_enemy_player(self.ecs_world, self.explosion_cfg['player'], self._lives_entity)
            system_explosion_state(self.ecs_world)
            system_animation(self.ecs_world, delta_time)
            system_respawn_player(self.ecs_world, self.player_entity, delta_time, self.spawn_player)

        
        #se optiene el numero de componentes
        componentEnemy = len(self.ecs_world.get_component(CTagEnemy))
        
        componentObject = self.ecs_world.get_components(CSurface, CTransform, CVelocity)


        if(componentEnemy == 0):
            create_level_text(self.ecs_world, self.interface_cfg, 'level_complete_text', TextAlignment.CENTER, TypeText.NEXT_LEVEL)
            create_level_text(self.ecs_world, self.interface_cfg, 'next_level_text', TextAlignment.CENTER, TypeText.NEXT_LEVEL)

            componentLevelText = self.ecs_world.get_components(CSurface, CTransform, CEndGameText)

            for _, (o_s, o_t, o_v) in componentObject:
                for _, (c_s, c_t, c_g) in componentLevelText:
                    self._leveltimecounter += delta_time
                    if self._leveltimecounter > delta_time:
                        c_s.surf.set_alpha(0)
                        continue
            
            for enemy in self.ecs_world.get_component(CTagEnemy):
                self.ecs_world.delete_entity(enemy)

            create_enemy_spawner(self.ecs_world, self.screen_rect)
            #self.switch_scene("LEVEL_02")


    def do_action(self, action: CInputCommand):
        velocity = self.player['input_velocity']

        if action.name == "PLAYER_LEFT":
            if action.phase == CommandPhase.START:
                self._player_cv.vel.x = -velocity
            elif action.phase == CommandPhase.END:
                self._player_cv.vel.x = 0

        if action.name == "PLAYER_RIGHT":
            if action.phase == CommandPhase.START:
                self._player_cv.vel.x = velocity
            elif action.phase == CommandPhase.END:
                self._player_cv.vel.x = 0

        if action.name == "PLAYER_FIRE":
            if action.phase == CommandPhase.START:
                bullet_entity = self.ecs_world.get_components(CTagBullet)
                player_entity_exists: bool = self.ecs_world.entity_exists(self.player_entity)

                if len(bullet_entity) == 0 and player_entity_exists:
                    ServiceLocator.sounds_service.play(self.player['sound'])
                    bullet_entity = create_player_bullet(
                        self.ecs_world, self.player_entity, self.player)
                    bullet_entity_c_v = self.ecs_world.component_for_entity(
                        bullet_entity, CVelocity)
                    bullet_entity_c_v.vel.y -= self.level_cfg['player_bullet_speed']

            elif action.phase == CommandPhase.END:
                pass

    def spawn_player(self):
        self.player_entity = create_player(self.ecs_world, self.screen_rect, self.player)
        self._player_tag = self.ecs_world.component_for_entity(self.player_entity, CTagPlayer)
        self._player_cv = self.ecs_world.component_for_entity(self.player_entity, CVelocity)
