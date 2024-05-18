import esper

from src.create.enemy_player_creator import create_enemy_explosion
from src.ecs.components.c_enemy_state import CEnemyState, EnemyState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_collision_bullet_enemy(world: esper.World, explosion_cfg: dict, player_tag: CTagPlayer):
    enemy = world.get_components(CSurface, CTransform, CTagEnemy, CEnemyState)
    bullet = world.get_components(CSurface, CTransform, CTagBullet)

    c_s: CSurface
    c_t: CTransform
    c_e: CEnemyState
    for enemy_entity, (c_s, c_t, _, c_e) in enemy:
        ene_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        for bullet_entity, (b_s, b_t, _) in bullet:
            bullet_rect = b_s.area.copy()
            bullet_rect.topleft = b_t.pos
            if ene_rect.colliderect(bullet_rect):

                if c_e.state == EnemyState.CHASING:
                    player_tag.score += c_e.chasing_score
                else:
                    player_tag.score += c_e.score

                player_tag.update_score = True
                create_enemy_explosion(world, c_t.pos, explosion_cfg)
                world.delete_entity(bullet_entity)
                world.delete_entity(enemy_entity)
