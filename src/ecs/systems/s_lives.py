import esper

from src.create.prefab_creator_interface import create_img_lives
from src.ecs.components.c_lives_counter import CLives
from src.ecs.components.tags.c_tag_live import CTagLive


def system_lives(world: esper.World, interface_cfg: dict, lives_entity: int):
    lives = world.component_for_entity(lives_entity, CLives)
    lives_components = world.get_components(CTagLive)

    flag: bool = False
    c_t: CTagLive
    for entity, (c_t) in lives_components:
        if lives.counter != len(lives_components):
            world.delete_entity(entity)
            flag = True

    if flag and lives.counter > 0:
        create_img_lives(world, interface_cfg, lives_entity)
