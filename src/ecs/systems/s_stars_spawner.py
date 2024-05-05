import esper
import random
from src.ecs.components.c_stars_spawner import CStarsSpawner, StarData
from src.ecs.components.c_surface import CSurface
from src.ecs.create.background_creator import create_star

def system_stars_spawner(world:esper.World, delta_time, screen_height):
    component = world.get_component(CStarsSpawner)
    c_ss:CStarsSpawner
    for _, c_ss in component:
        s_dt:StarData
        for s_dt in c_ss.start_data:
            s_dt.spawn_counter += delta_time
            if s_dt.spawn_counter > s_dt.spawn_at:
                if not s_dt.spawned:
                    s_dt.entity_id = create_star(world, s_dt.size, s_dt.pos, s_dt.vel, s_dt.col)
                    s_dt.spawned = True
                
                if s_dt.spawned:
                    entity = world.component_for_entity(s_dt.entity_id, CSurface)
                    num = random.random()
                    color = (0,0,0)
                    if (num <= 0.5):
                        color = s_dt.col
                    entity.surf.set_colorkey(color)

            if s_dt.pos.y > screen_height:
                s_dt.pos.y = 0
                s_dt.spawn_counter = 0
            