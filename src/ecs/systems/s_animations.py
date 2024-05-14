import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface

def system_animation(world:esper.World, delta_time:float):
    components = world.get_components(CSurface, CAnimation)
    c_s:CSurface
    c_a:CAnimation

    for _, (c_s, c_a) in components:
        c_a.curr_anim_time -= delta_time
        if c_a.curr_anim_time <=0:
            c_a.curr_anim_time = c_a.animation_list[c_a.curr_anim].framerate
            if c_a.reversed_animation:
                c_a.curr_frame -= 1
                if c_a.curr_frame < c_a.animation_list[c_a.curr_anim].end:
                    c_a.curr_frame = c_a.animation_list[c_a.curr_anim].start
            else:
                c_a.curr_frame += 1
                if c_a.curr_frame > c_a.animation_list[c_a.curr_anim].end:
                    c_a.curr_frame = c_a.animation_list[c_a.curr_anim].start

            rect_surf = c_s.surf.get_rect()
            c_s.area.w = rect_surf.w / c_a.number_frames
            c_s.area.x = c_s.area.w * c_a.curr_frame