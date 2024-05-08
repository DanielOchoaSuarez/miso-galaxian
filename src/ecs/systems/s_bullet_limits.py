import pygame
import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.create.enemy_player_creator import create_player_bullet


def system_bullet_limits(world:esper.World, screen:pygame.Surface, player_entity:int):
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CTagBullet)
    c_t:CTransform
    c_s:CSurface
    c_e:CTagBullet

    for bullet_entity, (c_t, c_s, c_e) in components:
        bull_rect = CSurface.get_area_relative(c_s.area, c_t.pos)    
        if bull_rect.top < 0 or bull_rect.bottom > screen_rect.height:
            world.delete_entity(bullet_entity)