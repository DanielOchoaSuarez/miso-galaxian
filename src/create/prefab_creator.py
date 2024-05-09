import pygame
import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def create_square(world: esper.World, size: pygame.Vector2, color: pygame.Color,
                  pos: pygame.Vector2, vel: pygame.Vector2) -> int:
    square_entity = world.create_entity()
    world.add_component(square_entity, CSurface(size, color))
    world.add_component(square_entity, CTransform(pos))
    if vel is not None:
        world.add_component(square_entity, CVelocity(vel))
    return square_entity


def create_sprite(world: esper.World, pos: pygame.Vector2, vel: pygame.Vector2,
                  surface: pygame.Surface) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity, CSurface.from_surface(surface))
    world.add_component(sprite_entity, CTransform(pos))
    if vel is not None:
        world.add_component(sprite_entity, CVelocity(vel))
    return sprite_entity
