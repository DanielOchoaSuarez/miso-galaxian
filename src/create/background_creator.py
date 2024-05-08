import esper
import pygame

from src.ecs.components.c_stars_spawner import CStarsSpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def create_star(
    world: esper.World,
    size: pygame.Vector2,
    pos: pygame.Vector2,
    vel: pygame.Vector2,
    col: pygame.color
) -> int:
    cuad_entity = world.create_entity()
    world.add_component(cuad_entity, CSurface(size=size, color=col))
    world.add_component(cuad_entity, CTransform(pos=pos))
    world.add_component(cuad_entity, CVelocity(vel=vel))
    return cuad_entity


def create_stars_spawner(world: esper.World, screen_rect: pygame.Rect):
    stars_spawner = world.create_entity()
    world.add_component(stars_spawner, CStarsSpawner(screen_rect))