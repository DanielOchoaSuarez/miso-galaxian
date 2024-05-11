import pygame
import esper
from src.ecs.components.c_enemy_spawner import CEnemySpawner, EnemyData
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_velocity import CVelocity

def system_enemy_idle_movement(world:esper.World, screen:pygame.Rect):
    component = world.get_component(CEnemySpawner)
    c_es:CEnemySpawner
    for _, c_es in component:
        e_dt = EnemyData

        # Check if at least one is closer to the edge of the screen
        # if so then change the flag and exit
        for e_dt in c_es.enemy_list:
            if not world.entity_exists(e_dt.entity_id):
                continue
            
            entity = world.component_for_entity(e_dt.entity_id, CSurface)
            enemy_rect = CSurface.get_area_relative(entity.area, e_dt.init_pos)
            if enemy_rect.left < c_es.reverse_limit and not c_es.should_reverse:
                c_es.should_reverse = True
                break
            if enemy_rect.right > (screen.width - c_es.reverse_limit) and c_es.should_reverse:
                c_es.should_reverse = False
                break

        # One by one change the direction of all enemies
        for e_dt in c_es.enemy_list:
            if not world.entity_exists(e_dt.entity_id):
                continue
            entity = world.component_for_entity(e_dt.entity_id, CVelocity)

            if c_es.should_reverse:
                entity.vel = c_es.r_l_velocity
            else:
                entity.vel = c_es.l_r_velocity
