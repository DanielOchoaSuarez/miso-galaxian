import src

from src.create.background_creator import create_stars_spawner
from src.create.enemy_player_creator import create_enemy_spawner, create_input_player, create_player, create_player_bullet
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.systems.s_animations import system_animation
from src.ecs.systems.s_bullet_limits import system_bullet_limits
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_enemy_idle_movement import system_enemy_idle_movement
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_explosion_state import system_explosion_state
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_limits import system_player_limits
from src.ecs.systems.s_stars_spawner import system_stars_spawner
from src.engine.cfg_loader import level_cfg, player_cfg, starfield_cfg, enemy_cfg, explosion_cfg
from src.engine.scenes.scene import Scene


class PlayScene(Scene):

    def __init__(self, level: str, engine: 'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)
        self.player = player_cfg()
        self.starfield_cfg = starfield_cfg()
        self.level_cfg = level_cfg(level)
        self.enemy_cfg = enemy_cfg()
        self.explosion_cfg = explosion_cfg()

    def do_create(self):
        create_stars_spawner(
            self.ecs_world, self.screen_rect, self.starfield_cfg)
        self.player_entity = create_player(
            self.ecs_world, self.screen_rect, self.player)
        self._player_tag = self.ecs_world.component_for_entity(self.player_entity, CTagPlayer)
        self._player_cv = self.ecs_world.component_for_entity(
            self.player_entity, CVelocity)
        create_input_player(self.ecs_world)
        create_enemy_spawner(self.ecs_world, self.screen_rect)

    def do_update(self, delta_time: float):
        system_stars_spawner(self.ecs_world, delta_time,
                            self.screen_rect.height)
        system_movement(self.ecs_world, delta_time, self.is_paused)
        if not self.is_paused:
            system_player_limits(self.ecs_world, self.screen_rect)
            system_bullet_limits(
                self.ecs_world, self.screen_rect, self.player_entity)
            system_enemy_spawner(self.ecs_world, self.screen_rect, self.enemy_cfg)
            system_enemy_idle_movement(self.ecs_world, self.screen_rect)
            system_collision_bullet_enemy(self.ecs_world, self.explosion_cfg['enemy'], self._player_tag)
            system_explosion_state(self.ecs_world)
            system_animation(self.ecs_world, delta_time)

    def do_action(self, action: CInputCommand):
        velocity = self.player['input_velocity']

        if action.name == "PLAYER_LEFT":
            if action.phase == CommandPhase.START:
                self._player_cv.vel.x -= velocity
            elif action.phase == CommandPhase.END:
                self._player_cv.vel.x += velocity

        if action.name == "PLAYER_RIGHT":
            if action.phase == CommandPhase.START:
                self._player_cv.vel.x += velocity
            elif action.phase == CommandPhase.END:
                self._player_cv.vel.x -= velocity

        if action.name == "PLAYER_FIRE":
            if action.phase == CommandPhase.START:
                bullet_entity = self.ecs_world.get_components(CTagBullet)
                if len(bullet_entity) == 0:
                    bullet_entity = create_player_bullet(
                        self.ecs_world, self.player_entity)
                    bullet_entity_c_v = self.ecs_world.component_for_entity(
                        bullet_entity, CVelocity)
                    bullet_entity_c_v.vel.y -= self.level_cfg['player_bullet_speed']
            elif action.phase == CommandPhase.END:
                pass
