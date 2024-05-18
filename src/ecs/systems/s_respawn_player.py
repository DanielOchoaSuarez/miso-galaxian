from typing import Callable
import esper
from src.ecs.components.c_game import CGame

def system_respawn_player(world: esper.World, player_entity:int, delta_time:float, respawn: Callable[[], None]):
    component = world.get_component(CGame)
    c_g:CGame
    for _, c_g in component:
        if not world.entity_exists(player_entity):
            if not c_g.is_respawning:
                c_g.life_respawn -= 1
                if c_g.life_respawn <= 0:
                    #game over
                    c_g.life_respawn = 0
                    break
                c_g.is_respawning = True

            c_g.respawn_counter += delta_time
            if c_g.respawn_counter >= c_g.time_to_respawn:
                c_g.respawn_counter = 0
                c_g.is_respawning = False
                respawn()
