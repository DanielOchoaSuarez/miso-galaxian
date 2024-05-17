import pygame
import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet


def system_bullet_limits(world: esper.World, screen_rect: pygame.Rect):
    player_bullets = world.get_components(CTransform, CSurface, CTagBullet)
    enemy_bullets = world.get_components(CTransform, CSurface, CTagEnemyBullet)

    c_t: CTransform
    c_s: CSurface
    c_tb: CTagBullet
    c_teb: CTagEnemyBullet

    for bullet_entity, (c_t, c_s, c_tb) in player_bullets:
        bull_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        if bull_rect.top < 0 or bull_rect.bottom > screen_rect.height:
            world.delete_entity(bullet_entity)

    for bullet_entity, (c_t, c_s, c_teb) in enemy_bullets:
        bull_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        if bull_rect.top < 0 or bull_rect.bottom > screen_rect.height:
            world.delete_entity(bullet_entity)
