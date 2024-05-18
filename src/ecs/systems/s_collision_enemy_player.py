import esper

from src.create.enemy_player_creator import create_player_explosion
from src.ecs.components.c_lives_counter import CLives
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_collision_enemy_player(world: esper.World, explosion_cfg: dict, lives_entity: int):
    enemy = world.get_components(CSurface, CTransform, CTagEnemy)
    player = world.get_components(CSurface, CTransform, CTagPlayer)
    lives = world.component_for_entity(lives_entity, CLives)

    c_s: CSurface
    c_t: CTransform
    for player_entity, (c_s, c_t, _) in player:
        player_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        for enemy_entity, (b_s, b_t, _) in enemy:
            enemy_rect = b_s.area.copy()
            enemy_rect.topleft = b_t.pos
            if player_rect.colliderect(enemy_rect):
                lives.counter -= 1
                create_player_explosion(world, c_t.pos, explosion_cfg)
                world.delete_entity(enemy_entity)
                world.delete_entity(player_entity)
