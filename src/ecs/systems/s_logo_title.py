import esper
import pygame


from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_logo_title import CTagLogoTitle


def system_logo_title(world: esper.World):

    components = world.get_components(CTransform, CVelocity, CTagLogoTitle)

    c_t: CTransform
    c_v: CVelocity
    c_title: CTagLogoTitle
    for _, (c_t, c_v, c_title) in components:

        pos = pygame.Vector2(
            c_t.pos.x - c_title.final_pos.x,
            c_t.pos.y - c_title.final_pos.y
        ).normalize()

        if pos.x <= 0 and pos.y <= 0:
            c_v.vel = pygame.Vector2(0, 0)
