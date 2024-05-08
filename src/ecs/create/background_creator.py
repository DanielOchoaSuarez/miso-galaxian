import pygame
import esper
from src.ecs.components.c_stars_spawner import CStarsSpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_star import CTagStar

def create_star(
        world:esper.World,
        size:pygame.Vector2,
        pos:pygame.Vector2,
        vel:pygame.Vector2,
        col:pygame.color
    ) -> int:
    cuad_entity = world.create_entity()
    world.add_component(cuad_entity, CSurface(size=size, color=col))
    world.add_component(cuad_entity, CTransform(pos=pos))
    world.add_component(cuad_entity, CVelocity(vel=vel))
    world.add_component(cuad_entity, CTagStar())
    return cuad_entity

def create_stars_spawner(world:esper.World, screen:pygame.Surface, starfield_cfg:dict):
    stars_spawner = world.create_entity()
    world.add_component(stars_spawner, CStarsSpawner(screen, starfield_cfg))