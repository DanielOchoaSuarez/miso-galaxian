import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_player_limits(world:esper.World, screen:pygame.Surface):
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CTagPlayer)
    c_t:CTransform
    c_s:CSurface
    c_e:CTagPlayer
    
    for entity, (c_t, c_s, c_e) in components:
        cuad_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        if screen_rect.colliderect(cuad_rect):
            cuad_rect.clamp_ip(screen_rect)
            c_t.pos.xy = cuad_rect
        