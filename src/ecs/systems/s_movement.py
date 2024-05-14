import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_star import CTagStar


def system_movement(world: esper.World, delta_time: float, is_paused: bool):
    if not is_paused:
        components = world.get_components(CTransform, CVelocity)

        c_t: CTransform
        c_v: CVelocity
        for _, (c_t, c_v) in components:
            c_t.pos.x += c_v.vel.x * delta_time
            c_t.pos.y += c_v.vel.y * delta_time
    else:
        components = world.get_components(CTransform, CVelocity, CTagStar)

        c_t: CTransform
        c_v: CVelocity
        for _, (c_t, c_v, _) in components:
            c_t.pos.x += c_v.vel.x * delta_time
            c_t.pos.y += c_v.vel.y * delta_time
