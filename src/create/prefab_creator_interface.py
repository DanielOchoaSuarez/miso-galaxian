import pygame
import esper


from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_logo_title import CTagLogoTitle
from src.engine.service_locator import ServiceLocator


def create_sprite(world: esper.World, pos: pygame.Vector2, vel: pygame.Vector2, surface: pygame.Surface) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity, CTransform(pos=pos))
    world.add_component(sprite_entity, CVelocity(vel=vel))
    world.add_component(sprite_entity, CSurface.from_surface(surface))
    return sprite_entity


def create_logo_title(world: esper.World, logo_info: dict) -> int:
    logo_sprite = ServiceLocator.images_service.get(logo_info['image'])
    size = logo_sprite.get_size()

    pos = pygame.Vector2(
        logo_info['position']['x'] - (size[0] / 2),
        logo_info['position']['y'] - (size[1] / 2))
    vel = pygame.Vector2(logo_info['vel']['x'], logo_info['vel']['y'])

    final_pos = pygame.Vector2(
        logo_info['final_position']['x'] - (size[0] / 2),
        logo_info['final_position']['y'] - (size[1] / 2))

    logo_entity = create_sprite(world, pos, vel, logo_sprite)
    world.add_component(logo_entity, CTagLogoTitle(final_pos=final_pos))
    return logo_entity
