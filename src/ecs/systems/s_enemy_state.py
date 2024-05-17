import esper
import pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_state import CEnemyState, EnemyState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.engine.service_locator import ServiceLocator

def system_enemy_state(world:esper.World, screen:pygame.Rect, player_entity:int, delta_time:float, level_cfg:dict):
    player_p = CTransform(pos=pygame.Vector2(screen.width / 2, screen.height + 20))
    player_v = CVelocity(vel=pygame.Vector2(0, 0))
    
    if world.entity_exists(player_entity):
        player_p = world.component_for_entity(player_entity, CTransform)
        player_v = world.component_for_entity(player_entity, CVelocity)

    components = world.get_components(CVelocity, CTransform, CSurface, CAnimation ,CEnemyState)

    c_v:CVelocity
    c_p:CTransform
    c_s:CSurface
    c_a:CAnimation
    c_es:CEnemyState
    for _, (c_v, c_p, c_s, c_a, c_es) in components:

        if c_es.state == EnemyState.MOVE:
            _do_move_state(c_v, c_p, c_a, c_es)

        elif c_es.state == EnemyState.CHASING:
            if c_es.sound_played == False:
                c_es.sound_played = True
                ServiceLocator.sounds_service.play(level_cfg['enemy_launch'])
            _do_chase_state(c_v, c_p, c_a, c_es, screen.height, player_p, player_v, delta_time)

        elif c_es.state == EnemyState.LANDING:
            _do_landing_state(c_v, c_p, c_s, c_a, c_es)

def _do_move_state(c_v:CVelocity, c_p:CTransform, c_a:CAnimation, c_es:CEnemyState):
    _set_animation(c_a, 0)
    c_es.state = EnemyState.CHASING
    c_v.vel = c_es.vel_chase

def _do_chase_state(c_v:CVelocity, c_p:CTransform, c_a:CAnimation, c_es:CEnemyState, screen_height, player_p:CTransform, player_v:CVelocity, delta_time):
    _set_animation(c_a, 0)
    player_offset_pos = pygame.Vector2((player_p.pos.x),(player_p.pos.y + 50))
    dist = c_p.pos.distance_to(player_offset_pos)
    desired_good_length = 80 / dist
    follow_vector = player_offset_pos - c_p.pos
    follow_vector.normalize_ip()
    follow_vector.scale_to_length(c_v.vel.magnitude())
    dir = follow_vector - c_v.vel
    dir *= desired_good_length
    c_v.vel = c_v.vel + dir
    if c_p.pos.y > screen_height:
        c_p.pos.y = 0
        c_es.state = EnemyState.LANDING

def _do_landing_state(c_v:CVelocity, c_p:CTransform, c_s:CSurface, c_a:CAnimation, c_es:CEnemyState):
    _set_animation(c_a, 0)
    vect = c_es.army_pos - c_p.pos
    vect.normalize_ip()
    c_v.vel = pygame.Vector2(100 * vect[0], 100 * vect[1])
    distance = c_p.pos.distance_to(c_es.army_pos)
    if distance < 1:
        c_v.vel = c_es.army_vel
        enemy_rect = CSurface.get_area_relative(c_s.area, c_es.army_pos)
        c_p.pos.xy = enemy_rect
        c_es.state = EnemyState.IDLE
        _set_animation(c_a, 0)

def _set_animation(c_a:CAnimation, anim:int):
    if c_a.curr_anim == anim:
        return
    
    c_a.curr_anim = anim
    c_a.curr_anim_time = 0
    c_a.curr_frame = c_a.animation_list[c_a.curr_anim].start
