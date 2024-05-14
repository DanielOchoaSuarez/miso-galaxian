import esper
import pygame


from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_menu_object import CMenuObject
from src.engine.scenes.scene import MenuSceneState


def system_menu_object(world: esper.World, delta_time: float, menu_state: MenuSceneState):
    components = world.get_components(
        CSurface, CTransform, CVelocity, CMenuObject)

    c_s: CSurface
    c_t: CTransform
    c_v: CVelocity
    c_m: CMenuObject
    for _, (c_s, c_t, c_v, c_m) in components:

        if menu_state == MenuSceneState.READY:

            origin = pygame.Vector2(0, 0)
            if c_m.alignment == 1:
                origin.x -= c_s.area.right

            elif c_m.alignment == 2:
                origin.x -= c_s.area.centerx

            c_t.pos = c_m.final_pos + origin
            c_v.vel = pygame.Vector2(0, 0)
        else:
            pos = pygame.Vector2(
                c_t.pos.x - c_m.final_pos.x,
                c_t.pos.y - c_m.final_pos.y
            ).normalize()

            if pos.x <= 0 and pos.y <= 0:
                c_v.vel = pygame.Vector2(0, 0)
                c_m.is_scrolled = True

        if c_m.blink:
            c_m.counter += delta_time

            if c_m.counter >= 0.6:
                c_m.counter = 0

                if c_s.surf.get_alpha() == 0:
                    c_s.surf.set_alpha(255)
                else:
                    c_s.surf.set_alpha(0)
