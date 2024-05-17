import esper
import pygame

from src.create.prefab_creator import create_sprite, create_square
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_enemy_state import CEnemyState
from src.ecs.components.c_explostion_state import CExplosionState
from src.ecs.components.c_game import CGame
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator


def create_player(world: esper.World, screen_rect: pygame.Rect, player_cfg: dict):
    player = ServiceLocator.images_service.get(player_cfg['image'])
    size = player.get_size()
    pos = pygame.Vector2(screen_rect.width / 2 -
                         (size[0]/2), screen_rect.height - 20)
    vel = pygame.Vector2(0, 0)
    player_entity = create_sprite(world, pos, vel, player)
    world.add_component(player_entity, CTagPlayer())
    return player_entity


def create_player_bullet(world: esper.World, player_entity: int, player_cfg:dict) -> int:
    p_s = world.component_for_entity(player_entity, CSurface)
    p_t = world.component_for_entity(player_entity, CTransform)
    ServiceLocator.sounds_service.play(player_cfg['sound'])
    player = p_s.surf.get_rect(topleft=p_t.pos)
    b_size = pygame.Vector2(1, 2)
    b_color = pygame.Color(255, 255, 255)
    b_pos = pygame.Vector2(player.center[0], p_t.pos.y)
    b_vel = pygame.Vector2(0, 0)
    bullet_entity = create_square(world, b_size, b_color, b_pos, b_vel)
    world.add_component(bullet_entity, CTagBullet())
    return bullet_entity

def create_enemy_bullet(world: esper.World, surface:CSurface, transform:CTransform, player_pos:pygame.Vector2) -> int:
    enemy = surface.surf.get_rect(topleft=transform.pos)
    b_size = pygame.Vector2(1, 2)
    b_color = pygame.Color(255, 255, 255)
    b_pos = pygame.Vector2((transform.pos.x + 5), (transform.pos.y + 10))
    b_vel = pygame.Vector2(100, 100)
    vect = player_pos - transform.pos
    vect.normalize_ip()
    new_vel = pygame.Vector2((b_vel[0] * vect[0]), (b_vel[1] * vect[1]))
    bullet_entity = create_square(world, b_size, b_color, b_pos, new_vel)
    world.add_component(bullet_entity, CTagEnemyBullet())
    return bullet_entity

def create_enemies(world:esper.World, pos:pygame.Vector2, on_idle_vel:pygame.Vector2, enemy:dict, reversed:str, reversed_flag:bool) -> int:
    enemy_surface = ServiceLocator.images_service.get(enemy['image'])
    enemy_sprite = create_sprite(world, pos, on_idle_vel, enemy_surface)
    world.add_component(enemy_sprite, CTagEnemy())
    world.add_component(enemy_sprite, CEnemyState(pos=pos.copy(), vel=on_idle_vel.copy(), chase=pygame.Vector2(enemy['velocity_chase'], enemy['velocity_chase'])))
    world.add_component(enemy_sprite, CAnimation(enemy['animations'][reversed], reversed_flag))
    return enemy_sprite

def create_enemy_explosion(world:esper.World, pos:pygame.Vector2, explosion_cfg):
    explosion_surf = ServiceLocator.images_service.get(explosion_cfg['image'])
    ServiceLocator.sounds_service.play(explosion_cfg['sound'])
    vel = pygame.Vector2(0, 0)
    explosion_entity = create_sprite(world, pos, vel, explosion_surf)
    world.add_component(explosion_entity, CTagExplosion())
    world.add_component(explosion_entity, CAnimation(explosion_cfg['animations'], False))
    world.add_component(explosion_entity, CExplosionState())

def create_player_explosion(world:esper.World, pos:pygame.Vector2, explosion_cfg):
    explosion_surf = ServiceLocator.images_service.get(explosion_cfg['image'])
    ServiceLocator.sounds_service.play(explosion_cfg['sound'])
    vel = pygame.Vector2(0, 0)
    explosion_entity = create_sprite(world, pos, vel, explosion_surf)
    world.add_component(explosion_entity, CTagExplosion())
    world.add_component(explosion_entity, CAnimation(explosion_cfg['animations'], False))
    world.add_component(explosion_entity, CExplosionState())

def create_game(world:esper.World):
    game_entity = world.create_entity()
    world.add_component(game_entity, CGame())

def create_input_player(world: esper.World):
    # Izquierda
    input_left = world.create_entity()
    world.add_component(input_left, CInputCommand(
        'PLAYER_LEFT', pygame.K_LEFT))

    # Derecha
    input_right = world.create_entity()
    world.add_component(input_right, CInputCommand(
        'PLAYER_RIGHT', pygame.K_RIGHT))

    # Disparo
    input_fire = world.create_entity()
    world.add_component(input_fire, CInputCommand(
        'PLAYER_FIRE', pygame.K_SPACE))

def create_enemy_spawner(world:esper.World, screen:pygame.Rect):
    enemy_spawner = world.create_entity()
    world.add_component(enemy_spawner, CEnemySpawner(screen))