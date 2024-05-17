import esper


from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_menu_object import CMenuObject


def system_paused_game(world: esper.World, delta_time: float, is_paused: bool):
    components = world.get_components(CSurface, CTransform, CMenuObject)

    c_s: CSurface
    c_t: CTransform
    c_m: CMenuObject
    for _, (c_s, c_t, c_m) in components:

        if not is_paused:
            c_s.surf.set_alpha(0)
            continue

        if c_m.blink:
            c_m.counter += delta_time

            if c_m.counter >= 0.6:
                c_m.counter = 0

                if c_s.surf.get_alpha() == 0:
                    c_s.surf.set_alpha(255)
                else:
                    c_s.surf.set_alpha(0)
