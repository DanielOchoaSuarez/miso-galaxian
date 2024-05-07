import pygame
import esper
import asyncio
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_velocity import CVelocity
from src.ecs.create.background_creator import create_stars_spawner
from src.ecs.create.enemy_player_creator import create_input_player, create_player
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_limits import system_player_limits
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_stars_spawner import system_stars_spawner
from src.engine.cfg_loader import *

class GameEngine:
    def __init__(self) -> None:
        title, size, self.framerate, self.bg_color = window_cfg()
        self.starfield = starfield_cfg()
        self.player = player_cfg()
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode((size['w'], size['h']), 0)
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.ecs_world = esper.World()
        self.is_running = False

    async def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            await asyncio.sleep(0)
        self._clean()

    def _create(self):
        create_stars_spawner(self.ecs_world, self.screen, self.starfield)
        self.player_entity = create_player(self.ecs_world, self.screen, self.player)
        self._player_cv = self.ecs_world.component_for_entity(self.player_entity, CVelocity)
        create_input_player(self.ecs_world)
        pass

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            system_input_player(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_stars_spawner(self.ecs_world, self.delta_time, self.screen.get_height())
        system_player_limits(self.ecs_world, self.screen)
        system_movement(self.ecs_world, self.delta_time)

    def _draw(self):
        self.screen.fill((self.bg_color['r'], self.bg_color['g'], self.bg_color['b']))
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()

    def _do_action(self, c_input:CInputCommand):
        velocity = self.player['input_velocity']

        if c_input.name == "PLAYER_LEFT":
            if c_input.phase == CommandPhase.START:
                self._player_cv.vel.x -= velocity
            elif c_input.phase == CommandPhase.END:
                self._player_cv.vel.x += velocity
        if c_input.name == "PLAYER_RIGHT":
            if c_input.phase == CommandPhase.START:
                self._player_cv.vel.x += velocity
            elif c_input.phase == CommandPhase.END:
                self._player_cv.vel.x -= velocity
        if c_input.name == "PLAYER_FIRE":
            if c_input.phase == CommandPhase.START:
                pass
            elif c_input.phase == CommandPhase.END:
                pass