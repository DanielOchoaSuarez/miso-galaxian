import pygame
import esper
from src.create.enemy_player_creator import create_enemies
from src.ecs.components.c_enemy_spawner import CEnemySpawner, EnemyData
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform

def system_enemy_spawner(world:esper.World, screen:pygame.Rect, enemies_cfg:dict):
    component = world.get_component(CEnemySpawner)
    c_es:CEnemySpawner
    for _, c_es in component:
        e_dt = EnemyData
        for e_dt in c_es.enemy_list:
            if not e_dt.is_spawned:
                reversed_type = 'normal'
                if e_dt.reversed_anim:
                    reversed_type = 'reversed'
                e_dt.entity_id = create_enemies(world, e_dt.init_pos, e_dt.on_idle_vel, enemies_cfg[e_dt.enemy_type], reversed_type, e_dt.reversed_anim)
                e_dt.is_spawned = True
