import asyncio
import pygame


from src.ecs.components.c_input_command import CInputCommand
from src.engine.cfg_loader import *
from src.engine.scenes.scene import Scene
from src.game.menu_scene import MenuScene
from src.game.play_scene import PlayScene


class GameEngine:
    def __init__(self) -> None:
        title, size, self._framerate, self.bg_color = window_cfg()

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(title)

        self.screen = pygame.display.set_mode(
            (size['w'], size['h']), pygame.SCALED)
        self.clock = pygame.time.Clock()
        self._delta_time = 0

        self.is_running = False
        self._scenes: dict[str, Scene] = {}
        self._scenes['MENU_SCENE'] = MenuScene(self)
        self._scenes["LEVEL_01"] = PlayScene("level_01.json", self)
        self._scenes["LEVEL_02"] = PlayScene("level_01.json", self)
        self._current_scene: Scene = None
        self._scene_name_to_switch: str = None

    async def run(self, start_scene_name: str) -> None:
        self.is_running = True
        self._current_scene = self._scenes[start_scene_name]
        self._create()

        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            self._handle_switch_scene()
            await asyncio.sleep(0)
        self._do_clean()

    def _create(self):
        self._current_scene.do_create()

    def _calculate_time(self):
        self.clock.tick(self._framerate)
        self._delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            self._current_scene.do_process_events(event)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        self._current_scene.simulate(self._delta_time)

    def _draw(self):
        self.screen.fill(
            (self.bg_color['r'], self.bg_color['g'], self.bg_color['b']))
        self._current_scene.do_draw(self.screen)
        pygame.display.flip()

    def _do_action(self, action: CInputCommand):
        self._current_scene.do_action(action)

    def _do_clean(self):
        if self._current_scene is not None:
            self._current_scene.clean()
        pygame.quit()

    def switch_scene(self, new_scene_name: str):
        self._scene_name_to_switch = new_scene_name

    def _handle_switch_scene(self):
        if self._scene_name_to_switch is not None:
            self._current_scene.clean()
            self._current_scene = self._scenes[self._scene_name_to_switch]
            self._current_scene.do_create()
            self._scene_name_to_switch = None
