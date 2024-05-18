import esper
import random
from src.create.enemy_player_creator import create_enemy_bullet
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_enemy_state import CEnemyState, EnemyState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform

def system_enemy_chasing(world:esper.World, delta_time:float, player_entity, screen_rect):
    component = world.get_component(CEnemySpawner)
    components = world.get_components(CSurface, CTransform, CEnemyState)
    player_p = None
    if world.entity_exists(player_entity):
        player_p = world.component_for_entity(player_entity, CTransform)
    
    c_s:CSurface
    c_t:CTransform
    c_est:CEnemyState
    c_es:CEnemySpawner
    for _, c_es in component:
        c_es.enemy_start_chase_counter += delta_time
        if c_es.enemy_start_chase_counter > c_es.enemy_start_chase:
            c_es.enemy_start_chase_counter = 0.0
            enemy_num = len(components)
            enemy_to_move = random.randint(0, enemy_num)
            counter = 0
            for _, (c_s, c_t, c_est) in components:

                if player_p is None:
                    continue
                
                if counter == enemy_to_move:
                    if c_est.state == EnemyState.IDLE:
                        c_est.state = EnemyState.MOVE
                        break
                counter += 1

        for _, (c_s, c_t, c_est) in components:

            if player_p is None:
                continue
            
            if c_est.state == EnemyState.CHASING:
                c_est.allow_shoot_time_counter += delta_time
                if c_est.allow_shoot_time_counter >= c_est.allow_shoot_time:
                    c_est.allow_shoot_time_counter = 0
                    if c_t.pos.y < (screen_rect.height - 50):
                        create_enemy_bullet(world, c_s, c_t, player_p.pos)
