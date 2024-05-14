import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_explostion_state import CExplosionState

def system_explosion_state(world:esper.World):
    components = world.get_components(CAnimation, CExplosionState)
    c_a:CAnimation
    for entity, (c_a, c_est) in components:
        if c_a.curr_frame == c_a.animation_list[c_a.curr_anim].end:
            world.delete_entity(entity)