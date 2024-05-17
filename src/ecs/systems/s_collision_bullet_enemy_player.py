import esper
from src.create.enemy_player_creator import create_enemy_explosion, create_player_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_collision_bullet_enemy_player(world:esper.World, explosion_cfg:dict):
    player = world.get_components(CSurface, CTransform, CTagPlayer)
    bullet = world.get_components(CSurface, CTransform, CTagEnemyBullet)
    c_s:CSurface
    c_t:CTransform

    for player_entity, (c_s, c_t, _) in player:
        player_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        for bullet_entity, (b_s, b_t, _) in bullet:
            bullet_rect = b_s.area.copy()
            bullet_rect.topleft = b_t.pos
            if player_rect.colliderect(bullet_rect):
                ## update lives counter
                create_player_explosion(world, c_t.pos, explosion_cfg)
                world.delete_entity(bullet_entity)
                world.delete_entity(player_entity)
