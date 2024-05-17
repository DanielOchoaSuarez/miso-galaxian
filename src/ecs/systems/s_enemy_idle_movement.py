import pygame
import esper
from src.ecs.components.c_enemy_spawner import CEnemySpawner, EnemyData
from src.ecs.components.c_enemy_state import CEnemyState, EnemyState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_enemy_idle_movement(world:esper.World, screen:pygame.Rect, delta_time:float):
    components = world.get_components(CVelocity, CTransform, CSurface, CEnemyState)
    c_v:CVelocity
    c_t:CTransform
    c_s:CSurface
    c_e:CEnemyState

    component = world.get_component(CEnemySpawner)
    c_es:CEnemySpawner
    
    for _, c_es in component:
        for _, (c_v, c_t, c_s, c_e) in components:
            enemy_rect = CSurface.get_area_relative(c_s.area, c_t.pos)

            if enemy_rect.left < c_es.reverse_limit and not c_es.should_reverse:
                c_es.should_reverse = True
                break
            if enemy_rect.right > (screen.width - c_es.reverse_limit) and c_es.should_reverse:
                c_es.should_reverse = False
                break
        
        for _, (c_v, c_t, c_s, c_e) in components:
            direction = None
            if c_es.should_reverse:
                direction = c_es.l_r_velocity
            else:
                direction = c_es.r_l_velocity

            c_e.army_pos.x += direction[0] * delta_time
            c_e.army_pos.y += direction[1] * delta_time
            c_e.army_vel = direction
            if c_e.state == EnemyState.IDLE:
                c_v.vel = direction
                


    # component = world.get_component(CEnemySpawner)
    # c_es:CEnemySpawner
    # for _, c_es in component:
    #     e_dt = EnemyData

    #     # Check if at least one is closer to the edge of the screen
    #     # if so then change the flag and exit
    #     for index, e_dt in enumerate(c_es.enemy_list):
    #         if not world.entity_exists(e_dt.entity_id):
    #             c_es.enemy_list.pop(index)
    #             continue
            
    #         entity = world.component_for_entity(e_dt.entity_id, CSurface)
    #         enemy_rect = CSurface.get_area_relative(entity.area, e_dt.init_pos)
    #         if enemy_rect.left < c_es.reverse_limit and not c_es.should_reverse:
    #             c_es.should_reverse = True
    #             break
    #         if enemy_rect.right > (screen.width - c_es.reverse_limit) and c_es.should_reverse:
    #             c_es.should_reverse = False
    #             break

    #     # One by one change the direction of all enemies
    #     for e_dt in c_es.enemy_list:
    #         entity = world.component_for_entity(e_dt.entity_id, CVelocity)

    #         if c_es.should_reverse:
    #             entity.vel = c_es.r_l_velocity
    #         else:
    #             entity.vel = c_es.l_r_velocity
