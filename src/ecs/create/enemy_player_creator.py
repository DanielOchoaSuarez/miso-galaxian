import esper
import pygame

from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.services.service_locator import ServiceLocator

def create_sprite(world:esper.World,
                  pos:pygame.Vector2,
                  vel:pygame.Vector2,
                  surface:pygame.Surface) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity, CTransform(pos=pos))
    world.add_component(sprite_entity, CVelocity(vel=vel))
    world.add_component(sprite_entity, CSurface.from_surface(surface=surface))
    return sprite_entity

def create_player(world:esper.World, screen:pygame.Surface, player_cfg:dict):
    player = ServiceLocator.images_service.get(player_cfg['image'])
    size = player.get_size()
    pos = pygame.Vector2(screen.get_width()/ 2 - (size[0]/2), screen.get_height() - 35)
    vel = pygame.Vector2(0, 0)
    player_entity = create_sprite(world, pos, vel, player)
    world.add_component(player_entity, CTagPlayer())
    return player_entity

def create_input_player(world:esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_fire = world.create_entity()
    world.add_component(input_left, CInputCommand('PLAYER_LEFT', pygame.K_LEFT))
    world.add_component(input_right, CInputCommand('PLAYER_RIGHT', pygame.K_RIGHT))
    world.add_component(input_fire, CInputCommand('PLAYER_FIRE', pygame.K_SPACE))
